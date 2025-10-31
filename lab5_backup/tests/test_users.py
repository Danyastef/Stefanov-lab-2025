import pytest
from flask import url_for

def test_users_index(client, example_users):
    response = client.get('/users/')
    assert response.status_code == 200
    response_text = response.get_data(as_text=True)
    
    for user in example_users:
        assert str(user.first_name) in response_text
        assert str(user.last_name) in response_text
        if user.middle_name is not None:
            assert str(user.middle_name) in response_text
        else:
            assert 'None' not in response_text

def test_show_existing_user(client, existing_user):
    client.post('/auth/login', data={'username': existing_user.username, 'password': 'qwerty'}, follow_redirects=True)
    response = client.get(f'/users/{existing_user.id}')
    assert response.status_code == 200
    assert existing_user.username in response.get_data(as_text=True)

def test_show_nonexisting_user(client):
    response = client.get('/users/999')
    assert response.status_code == 302  # Redirect
    # Follow redirect
    follow = client.get('/users/', follow_redirects=True)
    assert 'Пользователя нет в базе данных' in follow.get_data(as_text=True)

@pytest.mark.parametrize("user_data,expected_error", [
    ({'username': '', 'password': 'Password1!', 'first_name': 'Имя', 'last_name': 'Фамилия', 'role_id': '1'},
    'Поле не может быть пустым!'),
    ({'username': 'abc', 'password': 'Password1!', 'first_name': 'Имя', 'last_name': 'Фамилия', 'role_id': '1'},
    'Длина логина должна быть не менее 5 символов!'),
    ({'username': 'validuser', 'password': 'short', 'first_name': 'Имя', 'last_name': 'Фамилия', 'role_id': '1'},
    'Длина пароля должна быть от 8 до 128 символов!'),
])
def test_create_user_validation_errors(client, user_data, expected_error, existing_user):
    client.post('/login', data={'username': existing_user.username, 'password': 'qwerty'}, follow_redirects=True)
    response = client.post('/users/new', data=user_data, follow_redirects=True)
    assert expected_error in response.get_data(as_text=True)

def test_create_user_success(client, existing_user):
    client.post('/login', data={'username': existing_user.username, 'password': 'qwerty'}, follow_redirects=True)
    new_user_data = {
        'username': 'validuser',
        'password': 'Validpass1!',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'middle_name': '',
        'role_id': '1'
    }
    response = client.post('/users/new', data=new_user_data, follow_redirects=True)
    assert 'Учетная запись успешно создана' in response.get_data(as_text=True)

def test_delete_user(client, existing_user):
    client.post('/login', data={'username': existing_user.username, 'password': 'qwerty'}, follow_redirects=True)
    response = client.post(f'/users/{existing_user.id}/delete', follow_redirects=True)
    assert 'Учётная запись успешно удалена' in response.get_data(as_text=True)

def test_edit_user(client, existing_user):
    client.post('/login', data={'username': existing_user.username, 'password': 'qwerty'}, follow_redirects=True)
    updated_data = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'middle_name': 'Отчество',
        'role_id': '1'
    }
    response = client.post(f'/users/{existing_user.id}/edit', data=updated_data, follow_redirects=True)
    assert 'Учетная запись успешно изменена' in response.get_data(as_text=True)

def test_change_password(client, existing_user):
    client.post('/login', data={'username': existing_user.username, 'password': 'qwerty'}, follow_redirects=True)
    data = {
        'old_password': 'qwerty',
        'new_password': 'NewPass123!',
        'confirm_password': 'NewPass123!'
    }
    response = client.post('/users/change-password', data=data, follow_redirects=True)
    assert 'Пароль успешно изменён' in response.get_data(as_text=True)
