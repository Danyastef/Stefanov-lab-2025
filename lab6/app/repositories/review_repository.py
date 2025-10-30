from app.models import Review, Course
from sqlalchemy import select

class ReviewRepository:
    def __init__(self, db):
        self.db = db

    def get_last_reviews_for_course(self, course_id, limit = 5):
        query = (select(Review)
                .filter_by(course_id=course_id)
                .order_by(Review.created_at.desc())
                .limit(limit))
        return self.db.session.execute(query).scalars().all()
    
    def _all_query(self, course_id, sort_by='newest'):
        query = select(Review).filter_by(course_id=course_id)
        
        if sort_by == 'positive':
            query = query.order_by(Review.rating.desc(), Review.created_at.desc())
        elif sort_by == 'negative':
            query = query.order_by(Review.rating.asc(), Review.created_at.desc())
        else:
            query = query.order_by(Review.created_at.desc())
        return query
    
    def get_pagination_info(self, course_id, sort_by='newest'):
        query = self._all_query(course_id, sort_by)
        return self.db.paginate(query)
    
    def get_user_review_for_course(self, course_id, user_id):
        query = select(Review).filter_by(course_id=course_id, user_id=user_id)
        return self.db.session.execute(query).scalar()
    
    def create_review(self, course_id, user_id, rating, text):
        review = Review(
            course_id=course_id,
            user_id=user_id,
            rating=rating,
            text=text
        )
        
        self.db.session.add(review)
        
        course = self.db.session.get(Course, course_id)
        if course:
            course.rating_sum += rating
            course.rating_num += 1
        
        self.db.session.commit()
        return review