def test_get_by_id_with_existing_user(user_repository, existing_user):
    user = user_repository.get_by_id(existing_user.id)
    assert user.id == existing_user.id
    assert user.username == existing_user.username
    assert user.first_name == existing_user.first_name
    assert user.last_name == existing_user.last_name

def test_get_by_id_with_nonexisting_user(user_repository, nonexisting_user_id):
    user = user_repository.get_by_id(nonexisting_user_id)
    assert user is None

def test_all_with_nonempty_db(user_repository, example_users):
    users = user_repository.all()
    assert len(users) == len(example_users)
    for loaded_user, example_user in zip(users, example_users):
        assert loaded_user.id == example_user.id
        assert loaded_user.username == example_user.username

def test_get_by_username_and_password(user_repository, existing_user):
    user = user_repository.get_by_username_and_password(existing_user.username, 'qwerty')
    assert user is not None
    assert user.id == existing_user.id
    assert user.username == existing_user.username

def test_get_by_username_and_password_with_wrong_password(user_repository, existing_user):
    user = user_repository.get_by_username_and_password(existing_user.username, 'wrongpassword')
    assert user is None

def test_create_user(user_repository, existing_role):
    new_user_data = {
        'username': 'newuser',
        'password': 'newpass',
        'first_name': 'Смирнов',
        'middle_name': None,
        'last_name': 'Александрович',
        'role_id': existing_role.id
    }
    
    user_repository.create(**new_user_data)
    
    user = user_repository.get_by_username_and_password(new_user_data['username'], new_user_data['password'])
    assert user is not None
    assert user.username == new_user_data['username']
    assert user.first_name == new_user_data['first_name']
    assert user.last_name == new_user_data['last_name']
    assert user.role_id == new_user_data['role_id']

def test_update_user(user_repository, existing_user):
    updated_data = {
        'first_name': 'Updated',
        'middle_name': 'Middle',
        'last_name': 'Name',
        'role_id': existing_user.role_id
    }
    
    user_repository.update(existing_user.id, **updated_data)
    
    updated_user = user_repository.get_by_id(existing_user.id)
    assert updated_user.first_name == updated_data['first_name']
    assert updated_user.middle_name == updated_data['middle_name']
    assert updated_user.last_name == updated_data['last_name']
    assert updated_user.role_id == updated_data['role_id']

def test_update_password(user_repository, existing_user):
    new_password = 'newsecurepassword'
    user_repository.update_password(existing_user.id, new_password)
    
    user_with_old_pass = user_repository.get_by_username_and_password(existing_user.username, 'password123')
    assert user_with_old_pass is None
    
    user_with_new_pass = user_repository.get_by_username_and_password(existing_user.username, new_password)
    assert user_with_new_pass is not None
    assert user_with_new_pass.id == existing_user.id

def test_delete_user(user_repository, existing_user):
    user_repository.delete(existing_user.id)
    
    deleted_user = user_repository.get_by_id(existing_user.id)
    assert deleted_user is None