from app import check_phone_num

def test_url_args(client):
    response = client.get('/url_args?arg1=val1&arg2=val2')
    assert response.status_code == 200
    assert "arg1" in response.text
    assert "val1" in response.text
    assert "arg2" in response.text
    assert "val2" in response.text

def test_headers(client):
    response = client.get("/headers")
    assert response.status_code == 200
    for key, value in response.request.headers.items():
        assert key in response.text
        assert str(value) in response.text

def test_cookies(client):
    client.set_cookie(domain='localhost', key='test_cookie', value='test_value')
    response = client.get('/cookies')
    assert response.status_code == 200
    assert "test_cookie" in response.text
    assert "test_value" in response.text

    client.delete_cookie(key='test_cookie')
    response = client.get('/cookies')
    assert "test_cookie" not in response.text

def test_form(client):
    form_data = {
        'student_surname': 'Васильев',
        'student_name': 'Артём',
        'text': 'qwerty123'
    }
    response = client.post('/form', data=form_data)
    assert response.status_code == 200
    for k, v in form_data.items():
        assert k in response.text
        assert v in response.text

def test_check_phone_num():
    test_cases = [
        ("+7 (999) 123-45-67", "8-999-123-45-67"),
        ("999.123.45.67", "8-999-123-45-67"),
        ("89991234567", "8-999-123-45-67"),
        ("8(999)123-45-67", "8-999-123-45-67"),
        ("+7 999 123 45 67", "8-999-123-45-67"),
        ("8 999 123 45 67", "8-999-123-45-67"),
        ("+7.999.123.45.67", "8-999-123-45-67"),
        ("9991234567", "8-999-123-45-67"),
    ]
    
    for input_phone, expected_output in test_cases:
        assert check_phone_num(input_phone) == expected_output

def test_invalid_len_phone_check(client):
    response = client.post('/phone_check', data={'phone_num': '12345'})
    assert response.status_code == 200
    assert "is-invalid" in response.text
    assert "Недопустимый ввод. Неверное количество цифр." in response.text

def test_invalid_chars_phone_check(client):
    response = client.post('/phone_check', data={'phone_num': '12345f33'})
    assert response.status_code == 200
    assert "is-invalid" in response.text
    assert "Недопустимый ввод. В номере телефона встречаются недопустимые символы." in response.text

def test_client_phone_check(client):
    response = client.post('/phone_check', data={'phone_num': '+7 (999) 123-45-67'})
    assert response.status_code == 200
    assert "8-999-123-45-67" in response.text