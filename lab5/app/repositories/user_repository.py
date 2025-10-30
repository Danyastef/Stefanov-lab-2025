from sqlalchemy.orm import joinedload
from app.models import User

class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    def get_by_id(self, user_id):
        return self.db_connector.session.get(User, user_id)
    
    def get_by_username_and_password(self, username, password):
        user = self.db_connector.session.execute(
            self.db_connector.select(User).filter_by(username=username)
        ).scalar_one_or_none()
        if user and user.check_password(password):
            return user
        return None

    def all(self):
        return self.db_connector.session.execute(
            self.db_connector.select(User).options(joinedload(User.role))
        ).scalars().all()

    def create(self, username, password, first_name, middle_name, last_name, role_id):
        user = User(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            role_id=role_id
        )
        user.set_password(password)
        self.db_connector.session.add(user)
        self.db_connector.session.commit()
        return user

    def update(self, user_id, first_name, middle_name, last_name, role_id):
        user = self.db_connector.session.execute(
            self.db_connector.select(User).filter_by(id=user_id)
        ).scalar_one()
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.role_id = role_id
        self.db_connector.session.commit()
        return user

    def delete(self, user_id):
        user = self.db_connector.session.execute(
            self.db_connector.select(User).filter_by(id=user_id)
        ).scalar_one()
        self.db_connector.session.delete(user)
        self.db_connector.session.commit()

    def update_password(self, user_id, new_password):
        user = self.db_connector.session.execute(
            self.db_connector.select(User).filter_by(id=user_id)
        ).scalar_one()
        user.set_password(new_password)
        self.db_connector.session.commit()
