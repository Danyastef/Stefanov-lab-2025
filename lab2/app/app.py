from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app

def check_phone_num(phone_num):
    additional_chars = "1234567890 ()-.+"
    for p in phone_num:
        if p not in additional_chars:
            return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
    additional_chars = "1234567890+"
    num = ''.join(n for n in phone_num if n in additional_chars)
    if num.startswith('+7') or num.startswith('8'):
        if len(num.lstrip('+')) != 11:
            return "Недопустимый ввод. Неверное количество цифр."
        num = num.lstrip('+')[1:]
    else:
        if len(num) != 10:
            return "Недопустимый ввод. Неверное количество цифр."
    return f'8-{num[:3]}-{num[3:6]}-{num[6:8]}-{num[8:10]}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/url_args')
def url_args():
    return render_template('url_args.html', title='Параметры URL')

@app.route('/headers')
def headers():
    return render_template('headers.html', title='Заголовки запроса')

@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html', title='Cookie'))
    if 'name' not in request.cookies:
        resp.set_cookie('name', 'Stefanov Danil')
    else:
        resp.set_cookie('name', expires = 0)
    return resp

@app.route('/form', methods = ['GET', 'POST'])
def form():
    return render_template('form.html', title='Параметры формы')

@app.route('/phone_check', methods = ['GET', 'POST'])
def phone_check():
    error = None
    phone = None
    if request.method == 'POST':
        phone_num = request.form.get('phone_num', '').strip()
        result = check_phone_num(phone_num)
        if "Недопустимый ввод" in result:
            error = result
        else:
            phone = result
    
    return render_template('phone_check.html', title='Номер телефона', error=error, phone=phone)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)