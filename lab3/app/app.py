from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__)
application = app

app.secret_key = 'da4ba06f7e16bb5294eb76d6555d6a3df767f5e2a018bb6a264d4a23d6ffffe1'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к запрашиваемой странице необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'


def get_users():
    return [
        {
            'id': '1',
            'login': 'user',
            'password': 'qwerty'
        }
    ]

class User(UserMixin):
    def __init__(self, user_id, login):
        self.id = user_id
        self.login = login

@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user_id == user['id']:
            return User(user['id'], user['login'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/counter')
def counter():
    if session.get('counter'):
        session['counter'] += 1
    else:
        session['counter'] = 1
    return render_template('counter.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        next_page = request.args.get('next')
        if login and password:
            for user in get_users():
                if user['login'] == login and user['password'] == password:
                    user = User(user['id'], user['login'])
                    login_user(user, remember=remember_me)
                    flash('Вы успешно аутентифицированы.', 'success')
                    return redirect(next_page or url_for('index'))
            return render_template('login.html', error='Пользователь не найден')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)