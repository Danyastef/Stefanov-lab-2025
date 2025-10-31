from functools import wraps
from flask import Blueprint, request, render_template, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from app.policies.user_policy import UserPolicy
from app.repositories import UserRepository
from app.models import db


policies = {
    'users': UserPolicy
}

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйтесь для доступа к этому ресурсу.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user is not None:
        return user
    return None

@bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me', None) == 'on'

        user = user_repository.get_by_username_and_password(username, password)

        if user is not None:
            flash('Авторизация прошла успешно', 'success')
            login_user(user, remember=remember_me)
            next_url = request.args.get('next', url_for('index'))
            return redirect(next_url)
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.index'))

def can_user(resource, action, **kwargs):
    policy = policies[resource](**kwargs)
    return getattr(policy, action, lambda: False)()

def check_rights(resource, action):
    def decorator(function):
        @wraps(function)
        def wrapper(**kwargs):
            if not can_user(resource, action, **kwargs):
                flash('У вас недостаточно прав для доступа к данной странице.', 'warning')
                return redirect(url_for('users.index'))
            return function(**kwargs)
        return wrapper
    return decorator