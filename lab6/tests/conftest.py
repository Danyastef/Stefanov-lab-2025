import pytest
from flask import Flask, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash

from app.models import db, User, Course, Category, Review, Image
from app import create_app
from app.repositories import CourseRepository, UserRepository, ReviewRepository

TEST_DB_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://root:mospolytech@127.0.0.1/lab6_test',
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
def test_category(db_connector):
    category = Category(name='Математика')
    db_connector.session.add(category)
    db_connector.session.commit()
    yield category
    db_connector.session.delete(category)
    db_connector.session.commit()

@pytest.fixture
def test_image(db_connector):
    image = Image(
        id='test_img_123',
        file_name='test.jpg',
        mime_type='image/jpeg',
        md5_hash='testhash123'
    )
    db_connector.session.add(image)
    db_connector.session.commit()
    yield image
    db_connector.session.delete(image)
    db_connector.session.commit()

@pytest.fixture
def course_repository(db_connector):
    return CourseRepository(db_connector)

@pytest.fixture
def existing_course(db_connector, test_category, existing_user, test_image):
    course = Course(
        name='Тестовый курс',
        short_desc='Краткое описание',
        full_desc='Полное описание',
        category_id=test_category.id,
        author_id=existing_user.id,
        background_image_id=test_image.id,
        created_at=datetime.now()
    )
    db_connector.session.add(course)
    db_connector.session.commit()
    yield course
    db_connector.session.delete(course)
    db_connector.session.commit()

@pytest.fixture
def user_repository(db_connector):
    return UserRepository(db_connector)

@pytest.fixture
def existing_user(db_connector):
    user = User(
        id = 1,
        first_name='Иван',
        last_name='Иванов',
        login='user',
        password_hash=generate_password_hash('qwerty'),
        created_at=datetime.now()
    )
    db_connector.session.add(user)
    db_connector.session.commit()
    yield user
    db_connector.session.delete(user)
    db_connector.session.commit()

@pytest.fixture
def example_users(db_connector):
    users = [
        User(
            id=2,
            first_name='Иван',
            last_name='Иванов',
            login='user1',
            password_hash=generate_password_hash('qwerty'),
            created_at=datetime.now()
        ),
        User(
            id=3,
            first_name='Иван',
            last_name='Иванов',
            login='user2',
            password_hash=generate_password_hash('qwerty'),
            created_at=datetime.now()
        ),
        User(
            id=4,
            first_name='Иван',
            last_name='Иванов',
            login='user3',
            password_hash=generate_password_hash('qwerty'),
            created_at=datetime.now()
        )
    ]
    db_connector.session.add_all(users)
    db_connector.session.commit()
    yield users
    for user in users:
        db_connector.session.delete(user)
    db_connector.session.commit()

@pytest.fixture
def review_repository(db_connector):
    return ReviewRepository(db_connector)

@pytest.fixture
def existing_review(db_connector, existing_course, existing_user):
    review = Review(
        course_id=existing_course.id,
        user_id=existing_user.id,
        rating=5,
        text='Отзыв',
        created_at=datetime.now()
    )
    db_connector.session.add(review)
    db_connector.session.commit()
    yield review
    db_connector.session.delete(review)
    db_connector.session.commit()

@pytest.fixture
def client(app):
    return app.test_client()