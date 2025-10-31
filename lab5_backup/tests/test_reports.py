def login(client, username, password):
    return client.post('/auth/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_reports_index_access(client, existing_user):
    login(client, existing_user.username, 'qwerty')
    response = client.get('/reports/')
    assert response.status_code == 200
    assert 'Журнал посещений' in response.text

def test_by_pages_access(client, existing_user):
    login(client, existing_user.username, 'qwerty')
    response = client.get('/reports/by-pages')
    assert response.status_code == 200
    assert 'Количество посещений' in response.text

def test_export_by_pages(client, existing_user):
    login(client, existing_user.username, 'qwerty')
    response = client.get('/reports/by-pages/export')
    assert response.status_code == 200
    assert 'text/csv' in response.content_type
    assert 'Страница;Количество посещений' in response.data.decode('utf-8')

def test_by_users_access(client, existing_user):
    login(client, existing_user.username, 'qwerty')
    response = client.get('/reports/by-users')
    assert response.status_code == 200
    assert 'Пользователь' in response.text

def test_export_by_users(client, existing_user):
    login(client, existing_user.username, 'qwerty')
    response = client.get('/reports/by-users/export')
    assert response.status_code == 200
    assert 'text/csv' in response.content_type
    assert 'Пользователь;Количество посещений' in response.data.decode('utf-8')
