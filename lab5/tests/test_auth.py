import pytest
from flask import url_for

def test_login_success(client, existing_user):
    response = client.post('/auth/login', data={
        'username': existing_user.username,
        'password': 'qwerty',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Авторизация прошла успешно' in response.text


def test_login_failure_wrong_password(client, existing_user):
    response = client.post('/auth/login', data={
        'username': existing_user.username,
        'password': 'wrongpassword',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Неверное имя пользователя или пароль' in response.text


def test_login_failure_unknown_user(client):
    response = client.post('/auth/login', data={
        'username': 'unknownuser',
        'password': 'nopassword',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Неверное имя пользователя или пароль' in response.text


def test_logout(client, existing_user):
    client.post('/auth/login', data={
        'username': existing_user.username,
        'password': 'qwerty',
    }, follow_redirects=True)

    response = client.get('/auth/logout', follow_redirects=True)

    assert response.status_code == 200
    assert 'Пользователи' in response.text or response.request.path == '/users'


def test_login_remember_me(client, existing_user):
    response = client.post('/auth/login', data={
        'username': existing_user.username,
        'password': 'qwerty',
        'remember_me': 'on'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Авторизация прошла успешно' in response.text


def test_login_page_render(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert '<form' in response.text
