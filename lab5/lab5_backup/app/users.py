from flask import Blueprint, request, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
import mysql.connector as connector
from .repositories import UserRepository, RoleRepository
from app.models import db
from .auth import check_rights

def validate_user_input(data, required_fields=None):
    errors = {}

    if required_fields is None:
        required_fields = ['username', 'password', 'first_name', 'last_name']

    for field in required_fields:
        if not data.get(field):
            errors[field] = 'Поле не может быть пустым!'

    username = data.get('username')
    if username and 'username' in data:
        if len(username) < 5:
            errors['username'] = 'Длина логина должна быть не менее 5 символов!'
        elif not all(c.isalnum() and c.isascii() for c in username):
            errors['username'] = 'Логин должен содержать только латинские буквы и цифры!'

    password = data.get('password')
    if password and 'password' in data:
        allowed_symbols = set('~!?@#$%^&*_-+()[]{}></\\|"\'.,:')
        if len(password) < 8 or len(password) > 128:
            errors['password'] = 'Длина пароля должна быть от 8 до 128 символов!'
        elif not any(c.isupper() for c in password if c.isalpha()):
            errors['password'] = 'Пароль должен содержать хотя бы одну заглавную букву!'
        elif not any(c.islower() for c in password if c.isalpha()):
            errors['password'] = 'Пароль должен содержать хотя бы одну строчную букву!'
        elif not any(c.isdigit() for c in password):
            errors['password'] = 'Пароль должен содержать хотя бы одну цифру!'
        elif not all(c.isalpha() or c.isdigit() or c in allowed_symbols for c in password):
            errors['password'] = 'Пароль содержит недопустимые символы!'
        elif ' ' in password:
            errors['password'] = 'Пароль не должен содержать пробелов!'

    return errors

user_repository = UserRepository(db)
role_repository = RoleRepository(db)

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def index():
    return render_template('users/index.html', users=user_repository.all())

@bp.route('/<int:user_id>')
@login_required
@check_rights('users', 'show')
def show(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        flash('Пользователя нет в базе данных', 'danger')
        return redirect(url_for('users.index'))
    user_role = role_repository.get_by_id(user.role_id)
    return render_template('users/show.html', user_data=user, user_role=getattr(user_role, 'name', ''))

@bp.route('/new', methods = ['POST', 'GET'])
@login_required
@check_rights('users', 'create')
def new():
    user_data = {}
    errors = {}
    if request.method == 'POST':
        fields = {'username', 'password', 'first_name', 'middle_name', 'last_name', 'role_id'}
        user_data = { field: request.form.get(field) or None for field in fields}
        errors = validate_user_input(user_data)
        if not errors:
            try:
                user_repository.create(**user_data)
                flash('Учетная запись успешно создана', 'success')
                return redirect(url_for('users.index'))
            except connector.errors.DatabaseError:
                flash('Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены', 'danger')
                db.connect().rollback()
    return render_template('users/new.html', user_data=user_data, roles=role_repository.all(), errors=errors)

@bp.route('/<int:user_id>/delete', methods = ['POST'])
@login_required
@check_rights('users', 'delete')
def delete(user_id):
    try:
        user = user_repository.get_by_id(user_id)
        if user is None:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('users.index'))
            
        user_repository.delete(user_id)
        flash('Учётная запись успешно удалена', 'success')
    except connector.errors.DatabaseError:
        flash('Произошла ошибка при удалении учетной записи. Пожалуйста, попробуйте позже.', 'danger')
    
    return redirect(url_for('users.index'))

@bp.route('/<int:user_id>/edit', methods = ['POST', 'GET'])
@login_required
@check_rights('users', 'edit')
def edit(user_id):
    user = user_repository.get_by_id(user_id)
    print(user)
    if user is None:
        flash('Пользователя нет в базе данных', 'danger')
        return redirect(url_for('users.index'))
    
    errors = {}

    if request.method == 'POST':
        fields = {'first_name', 'middle_name', 'last_name', 'role_id'}
        user_data = { field: request.form.get(field) or None for field in fields}
        user_data['user_id'] = user_id
        validation_fields = {key: user_data[key] for key in ['first_name', 'last_name']}
        errors = validate_user_input(validation_fields, required_fields=['first_name', 'last_name'])
        if not errors:
            try:
                user_repository.update(**user_data)
                flash('Учетная запись успешно изменена', 'success')
                return redirect(url_for('users.index'))
            except connector.errors.DatabaseError:
                flash('Произошла ошибка при изменении записи.', 'danger')
                db.connect().rollback()
                user = user_data
        else:
            print(validation_fields)
    readonly_role = current_user.role.name == 'user'
    return render_template('users/edit.html', user_data=user, roles=role_repository.all(), errors=errors, readonly_role=readonly_role)

@bp.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password():
    errors = {}
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        user = user_repository.get_by_id(current_user.id)
        valid_user = user_repository.get_by_username_and_password(user.username, old_password)
        if not valid_user:
            errors['old_password'] = 'Старый пароль введён неверно!'

        if new_password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают!'

        password_errors = validate_user_input({'password': new_password})
        if 'password' in password_errors:
            errors['new_password'] = password_errors['password']

        if not errors:
            try:
                user_repository.update_password(current_user.id, new_password)
                flash('Пароль успешно изменён', 'success')
                return redirect(url_for('index'))
            except connector.errors.DatabaseError:
                db.connect().rollback()
                flash('Произошла ошибка при изменении пароля.', 'danger')

    return render_template('users/change_password.html', errors=errors)