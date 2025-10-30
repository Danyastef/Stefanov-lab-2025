import pytest
from flask import session, url_for
from app import app as application

@pytest.fixture
def app():
    return application

@pytest.fixture
def client(app):
    return app.test_client()

def test_counter1(client):
    response1 = client.get("/counter")
    assert "Вы посетили эту страницу 1 раз!" in response1.text
    with client.session_transaction() as sess:
        sess.clear()
    response2 = client.get("/counter")
    assert "Вы посетили эту страницу 1 раз!" in response2.text

def test_counter2(client):
    client.get("/counter")
    client.get("/counter")
    response = client.get("/counter")
    assert "Вы посетили эту страницу 3 раз!" in response.text    

def test_login_success(client):
    response = client.post("/login", data={"username": "user", "password": "qwerty"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Вы успешно аутентифицированы." in response.text
    assert response.request.path == "/"

def test_login_unsuccess(client):
    response = client.post("/login", data={"username": "user", "password": "123"})
    assert response.status_code == 200
    assert "Пользователь не найден" in response.text
    assert response.request.path == "/login"

def test_auth_secret(client):
    client.post("/login", data={"username": "user", "password": "qwerty"})
    response = client.get("/secret")
    assert response.status_code == 200
    assert "Доступ к этой странице имеют только авторизованные пользователи." in response.text

def test_unauth_secret(client):
    response = client.get("/secret", follow_redirects=True)
    assert response.status_code == 200
    assert "Для доступа к запрашиваемой странице необходимо пройти процедуру аутентификации." in response.text
    assert response.request.path == "/login"

def test_login_secret(client):
    response = client.get("/secret", follow_redirects=True)
    assert "Для доступа к запрашиваемой странице необходимо пройти процедуру аутентификации." in response.text
    assert response.request.path == "/login"
    response = client.post("/login?next=%2Fsecret", data={"username": "user", "password": "qwerty"}, follow_redirects=True)
    assert response.request.path == "/secret"
    assert "Вы успешно аутентифицированы." in response.text
    assert "Доступ к этой странице имеют только авторизованные пользователи." in response.text

def test_remember_me(client):
    response = client.post("/login", data={"username": "user", "password": "qwerty", "remember_me": "on"}, follow_redirects=True)
    assert response.status_code == 200
    response = client.get("/")
    assert 'remember_token' in response.request.headers.get("Cookie", "")

def test_navbar_auth(client):
    response = client.get("/")
    assert "Войти" in response.text
    assert "Выйти" not in response.text
    assert '<a class="nav-link" aria-current="page" href="/secret">Секрет</a>' not in response.text

def test_navber_unauth(client):
    client.post("/login", data={"username": "user", "password": "qwerty"})
    response = client.get("/")
    assert "Войти" not in response.text
    assert "Выйти" in response.text
    assert '<a class="nav-link" aria-current="page" href="/secret">Секрет</a>' in response.text