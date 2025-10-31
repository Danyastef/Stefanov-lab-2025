import pytest
from flask import Flask
from datetime import datetime, timedelta
from app import create_app
from app.models import db, Role, User, VisitLog
from app.repositories import RoleRepository, UserRepository
from werkzeug.security import generate_password_hash

TEST_DB_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://root:mospolytech@127.0.0.1/lab5_test',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'TESTING': True
}

@pytest.fixture(scope='session')
def app():
    app = create_app(TEST_DB_CONFIG)
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def _db(app):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

@pytest.fixture
def db_connector(_db):
    return _db

@pytest.fixture
def role_repository(db_connector):
    return RoleRepository(db_connector)

@pytest.fixture
def existing_role(db_connector):
    role = Role(id=1, name='admin')
    db_connector.session.add(role)
    db_connector.session.commit()
    yield role
    db_connector.session.delete(role)
    db_connector.session.commit()

@pytest.fixture
def nonexisting_role_id():
    return 999

@pytest.fixture
def example_roles(db_connector):
    roles = [
        Role(id=2, name='admin'),
        Role(id=3, name='test')
    ]
    db_connector.session.add_all(roles)
    db_connector.session.commit()
    yield roles
    for role in roles:
        db_connector.session.delete(role)
    db_connector.session.commit()

@pytest.fixture
def user_repository(db_connector):
    return UserRepository(db_connector)

@pytest.fixture
def existing_user(db_connector, existing_role):
    user = User(
        id=1,
        username='user1',
        first_name='Иван',
        last_name='Иванов',
        middle_name=None,
        password_hash=generate_password_hash('qwerty'),
        role_id=existing_role.id
    )
    db_connector.session.add(user)
    db_connector.session.commit()
    yield user
    db_connector.session.delete(user)
    db_connector.session.commit()

@pytest.fixture
def nonexisting_user_id():
    return 999

@pytest.fixture
def user_role(db_connector):
    role = Role(id=2, name='user')
    db_connector.session.add(role)
    db_connector.session.commit()
    yield role
    db_connector.session.delete(role)
    db_connector.session.commit()

@pytest.fixture
def example_users(db_connector, existing_role, user_role):
    users = [
        User(
            id=1,
            username='user1',
            first_name='Иван',
            last_name='Иванов',
            middle_name=None,
            password_hash=generate_password_hash('pass1'),
            role_id=existing_role.id
        ),
        User(
            id=2,
            username='user2',
            first_name='Пётр',
            last_name='Петров',
            middle_name='Петрович',
            password_hash=generate_password_hash('pass2'),
            role_id=None
        ),
        User(
            id=3,
            username='user3',
            first_name='Андрей',
            last_name='Сидоров',
            middle_name=None,
            password_hash=generate_password_hash('pass3'),
            role_id=existing_role.id
        ),
        User(
            id=4,
            username='user4',
            first_name='Василий',
            last_name='Брежнев',
            middle_name=None,
            password_hash=generate_password_hash('pass4'),
            role_id=user_role.id
        )
    ]
    db_connector.session.add_all(users)
    db_connector.session.commit()
    yield users
    for user in users:
        db_connector.session.delete(user)
    db_connector.session.commit()

@pytest.fixture
def existing_visit_log(db_connector, existing_user):
    visit = VisitLog(
        id=1,
        path='/test',
        user_id=existing_user.id,
        created_at=datetime.now()
    )
    db_connector.session.add(visit)
    db_connector.session.commit()
    yield visit
    db_connector.session.delete(visit)
    db_connector.session.commit()

@pytest.fixture
def anonymous_visit_log(db_connector):
    visit = VisitLog(
        id=2,
        path='/anonymous',
        user_id=None,
        created_at=datetime.now()
    )
    db_connector.session.add(visit)
    db_connector.session.commit()
    yield visit
    db_connector.session.delete(visit)
    db_connector.session.commit()

@pytest.fixture
def example_visit_logs(db_connector, existing_user):
    visits = [
        VisitLog(
            path='/page1',
            user_id=existing_user.id,
            created_at=datetime.now() - timedelta(minutes=10)
        ),
        VisitLog(
            path='/page2',
            user_id=None,
            created_at=datetime.now() - timedelta(minutes=5)
        ),
        VisitLog(
            path='/page3',
            user_id=existing_user.id,
            created_at=datetime.now()
        )
    ]
    db_connector.session.add_all(visits)
    db_connector.session.commit()
    yield visits
    for visit in visits:
        db_connector.session.delete(visit)
    db_connector.session.commit()

@pytest.fixture
def client(app):
    return app.test_client()