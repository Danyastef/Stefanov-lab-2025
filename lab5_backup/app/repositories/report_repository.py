from app.models import db, VisitLog, User
from sqlalchemy import func, literal, text
from flask_login import current_user

class ReportRepository:
    def get_visits_page(page, per_page=10):
        return db.session.query(VisitLog).join(User, isouter=True).order_by(VisitLog.created_at.desc()).paginate(page=page, per_page=per_page)

    def get_page_stats():
        return db.session.query(
            VisitLog.path,
            func.count().label("count")
        ).group_by(VisitLog.path).order_by(func.count().desc()).all()

    def get_user_stats():
        user_stats = db.session.query(
            User.last_name,
            User.first_name,
            User.middle_name,
            VisitLog.user_id,
            func.count().label("count")
        ).join(VisitLog, VisitLog.user_id == User.id).group_by(User.id)

        anon_stats = db.session.query(
            literal("Анонимный").label("last_name"),
            literal("пользователь").label("first_name"),
            literal("").label("middle_name"),
            literal(None).label("user_id"),
            func.count().label("count")
        ).filter(VisitLog.user_id.is_(None))
        
        return user_stats.union(anon_stats).order_by(text("count DESC")).all()

    def get_anonymous_visits_count():
        return db.session.query(
            func.count()
        ).filter(VisitLog.user_id.is_(None)).scalar()
    
    def get_paginated_visits(page=1, per_page=10, filters=None, order_by=None, policy=None):
        query = db.session.query(VisitLog).join(User, isouter=True)
        
        if policy:
            query = policy.view_journal(query) or query.filter(False)
        
        if filters:
            for field, value in filters.items():
                if hasattr(VisitLog, field):
                    query = query.filter(getattr(VisitLog, field) == value)
        
        if order_by and hasattr(VisitLog, order_by):
            query = query.order_by(getattr(VisitLog, order_by).desc())
        else:
            query = query.order_by(VisitLog.created_at.desc())
        
        return query.paginate(page=page, per_page=per_page, error_out=False)