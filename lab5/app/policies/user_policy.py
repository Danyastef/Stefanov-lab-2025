from flask_login import current_user
from .base_policy import BasePolicy, authentication_required
from app.repositories import UserRepository
from app.models import db, VisitLog

user_repository = UserRepository(db)

class UserPolicy(BasePolicy):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')

    @authentication_required
    def show(self):
        if current_user.role.name == 'admin':
            return True
        if current_user.role.name == 'user':
            return self.user_id == current_user.id
        return False
    
    @authentication_required
    def create(self):
        if current_user.role.name == 'admin':
            return True
        return False
    
    @authentication_required
    def edit(self):
        if current_user.role.name == 'admin':
            return True
        if current_user.role.name == 'user':
            return self.user_id == current_user.id
        return False
    
    @authentication_required
    def delete(self):
        if current_user.role.name == 'admin':
            return True
        return False
        
    @authentication_required
    def view_journal(self, query=None):
        if current_user.role.name == 'admin':
            return query if query is not None else True
        if current_user.role.name == 'user':
            if query is not None:
                return query.filter(VisitLog.user_id == current_user.id)
            return True
        return False
    
    @authentication_required
    def view_journal_analytics(self):
        if current_user.role.name == 'admin':
            return True
        return False