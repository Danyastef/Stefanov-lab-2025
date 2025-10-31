import pytest
from flask import url_for

def test_admin_can_view_any_user(client, existing_user, existing_role, db_connector):
    existing_role.name = 'admin'
    db_connector.session.commit()
    
    client.post('/auth/login', 
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get(f'/users/{existing_user.id}')
    assert response.status_code == 200

def test_user_can_view_own_profile(client, existing_user, existing_role, db_connector):
    existing_role.name = 'user'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get(f'/users/{existing_user.id}')
    assert response.status_code == 200

def test_user_cannot_view_other_profile(client, example_users, user_role, db_connector):
    current_user = example_users[3]
    current_user.role_id = user_role.id
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': current_user.username, 'password': 'pass4'},
            follow_redirects=True)
    
    other_user = example_users[0]
    response = client.get(f'/users/{other_user.id}', follow_redirects=True)
    assert 'У вас недостаточно прав' in response.get_data(as_text=True)

def test_anonymous_cannot_view_profiles(client, existing_user):
    response = client.get(f'/users/{existing_user.id}', follow_redirects=True)
    assert response.status_code == 200
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_admin_can_create_users(client, existing_user, existing_role, db_connector):
    existing_role.name = 'admin'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get('/users/new')
    assert response.status_code == 200

def test_user_cannot_create_users(client, existing_user, existing_role, db_connector):
    existing_role.name = 'user'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get('/users/new', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_anonymous_cannot_create_users(client):
    response = client.get('/users/new', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_admin_can_edit_any_user(client, existing_user, existing_role, db_connector):
    existing_role.name = 'admin'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get(f'/users/{existing_user.id}/edit')
    assert response.status_code == 200

def test_user_can_edit_own_profile(client, existing_user, existing_role, db_connector):
    existing_role.name = 'user'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get(f'/users/{existing_user.id}/edit')
    assert response.status_code == 200

def test_user_cannot_edit_other_profile(client, example_users, user_role, db_connector):
    current_user = example_users[3]
    current_user.role_id = user_role.id
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': current_user.username, 'password': 'pass4'},
            follow_redirects=True)
    
    other_user = example_users[0]
    response = client.get(f'/users/{other_user.id}/edit', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_anonymous_cannot_edit_profiles(client, existing_user):
    response = client.get(f'/users/{existing_user.id}/edit', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_admin_can_delete_users(client, existing_user, existing_role, db_connector):
    existing_role.name = 'admin'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.post(f'/users/{existing_user.id}/delete', follow_redirects=True)
    assert 'Учётная запись успешно удалена' in response.get_data(as_text=True)

def test_user_cannot_delete_users(client, example_users, user_role, db_connector):
    current_user = example_users[3]
    current_user.role_id = user_role.id
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': current_user.username, 'password': 'pass4'},
            follow_redirects=True)
    
    other_user = example_users[0]
    response = client.post(f'/users/{other_user.id}/delete', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_anonymous_cannot_delete_users(client, existing_user):
    response = client.post(f'/users/{existing_user.id}/delete', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_admin_can_view_all_visit_logs(client, existing_user, existing_role, example_visit_logs, db_connector):
    existing_role.name = 'admin'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get('/reports/')
    assert response.status_code == 200
    assert all(page in response.get_data(as_text=True) for page in ['/page1', '/page2', '/page3'])

def test_user_can_view_only_own_visit_logs(client, example_users, user_role, db_connector):
    current_user = example_users[3]
    current_user.role_id = user_role.id
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': current_user.username, 'password': 'pass4'},
            follow_redirects=True)
    
    response = client.get('/reports/')
    assert response.status_code == 200
    assert '/page2' not in response.get_data(as_text=True)

def test_admin_can_view_analytics(client, existing_user, existing_role, db_connector):
    existing_role.name = 'admin'
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': existing_user.username, 'password': 'qwerty'},
            follow_redirects=True)
    
    response = client.get('/reports/by-users')
    assert response.status_code == 200

def test_user_cannot_view_analytics(client, example_users, user_role, db_connector):
    current_user = example_users[3]
    current_user.role_id = user_role.id
    db_connector.session.commit()
    
    client.post('/auth/login',
            data={'username': current_user.username, 'password': 'pass4'},
            follow_redirects=True)
    
    response = client.get('/reports/by-users', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)

def test_anonymous_cannot_view_analytics(client):
    response = client.get('/reports/by-users', follow_redirects=True)
    assert 'У вас недостаточно прав для доступа к данной странице.' in response.get_data(as_text=True)