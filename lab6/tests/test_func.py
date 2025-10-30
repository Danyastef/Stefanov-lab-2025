import pytest
from app.models import Review

def test_get_last_reviews_for_course(review_repository, existing_review, existing_course):
    reviews = review_repository.get_last_reviews_for_course(existing_course.id)
    assert len(reviews) == 1
    assert reviews[0].id == existing_review.id

def test_get_pagination_info(review_repository, existing_review, existing_course):
    pagination = review_repository.get_pagination_info(existing_course.id)
    assert pagination.total == 1
    assert pagination.items[0].id == existing_review.id

def test_get_user_review_for_course(review_repository, existing_review, existing_course, existing_user):
    review = review_repository.get_user_review_for_course(existing_course.id, existing_user.id)
    assert review.id == existing_review.id

def test_create_review(db_connector, review_repository, existing_course, existing_user, existing_review):
    initial_sum = existing_course.rating_sum
    initial_num = existing_course.rating_num
    review = review_repository.create_review(
        course_id=existing_course.id,
        user_id=existing_user.id,
        rating=4,
        text="Отзыв2"
    )
    
    assert review.id is not None
    assert review.text == "Отзыв2"
    assert review.rating == 4
    assert existing_course.rating_sum == initial_sum + 4
    assert existing_course.rating_num == initial_num + 1

    db_connector.session.delete(review)
    db_connector.session.commit()


def test_show_course_with_reviews(client, existing_course, existing_review):
    response = client.get(f'/courses/{existing_course.id}')
    assert response.status_code == 200
    assert str(existing_review.rating).encode() in response.data
    assert existing_review.text.encode() in response.data

def test_reviews_page(client, existing_course, existing_review):
    response = client.get(f'/courses/{existing_course.id}/reviews')
    assert response.status_code == 200
    assert str(existing_review.rating).encode() in response.data
    assert existing_review.text.encode() in response.data

def test_user_create_review(db_connector, client, existing_course, existing_user):
    client.post('/auth/login', data={
        'login': existing_user.login,
        'password': 'qwerty'
    }, follow_redirects=True)

    client.post(
        f'/courses/{existing_course.id}/reviews/create',
        data={'rating': '4', 'text': 'Хороший курс!'},
        follow_redirects=True
    )
    response = client.get(f'/courses/{existing_course.id}/reviews')
    assert response.status_code == 200
    assert 'Хороший курс!' in response.text

    review = db_connector.session.query(Review).filter_by(
        course_id=existing_course.id,
        user_id=existing_user.id,
        text='Хороший курс!'
    ).first()
    assert review is not None
    
    db_connector.session.delete(review)
    db_connector.session.commit()

def test_sorting_reviews(db_connector, review_repository, existing_course, example_users):
    review1 = review_repository.create_review(
        course_id=existing_course.id,
        user_id=example_users[0].id,
        rating=1,
        text="Плохой курс"
    )
    
    review2 = review_repository.create_review(
        course_id=existing_course.id,
        user_id=example_users[1].id,
        rating=3,
        text="Курс не очень хороший"
    )

    review3 = review_repository.create_review(
        course_id=existing_course.id,
        user_id=example_users[2].id,
        rating=5,
        text="Отличный курс"
    )
    
    newest = review_repository.get_pagination_info(existing_course.id, 'newest')
    assert newest.items[0].id == review1.id
    
    positive = review_repository.get_pagination_info(existing_course.id, 'positive')
    assert [r.rating for r in positive.items] == [5, 3, 1]
    
    negative = review_repository.get_pagination_info(existing_course.id, 'negative')
    assert [r.rating for r in negative.items] == [1, 3, 5]

    db_connector.session.delete(review1)
    db_connector.session.delete(review2)
    db_connector.session.delete(review3)
    db_connector.session.commit()

def test_user_can_create_only_one_review_per_course(db_connector, client, existing_course, existing_user):
    client.post('/auth/login', data={
        'login': existing_user.login,
        'password': 'qwerty'
    }, follow_redirects=True)

    response = client.post(
        f'/courses/{existing_course.id}/reviews/create',
        data={'rating': '4', 'text': 'Первый отзыв'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Первый отзыв' in response.text

    response = client.post(
        f'/courses/{existing_course.id}/reviews/create',
        data={'rating': '2', 'text': 'Второй отзыв'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Вы уже оставляли отзыв на данный курс!' in response.text
    assert 'Второй отзыв' not in response.text

    reviews = db_connector.session.query(Review).filter_by(
        course_id=existing_course.id,
        user_id=existing_user.id
    ).all()
    assert len(reviews) == 1
    assert reviews[0].text == 'Первый отзыв'

    db_connector.session.delete(reviews[0])
    db_connector.session.commit()