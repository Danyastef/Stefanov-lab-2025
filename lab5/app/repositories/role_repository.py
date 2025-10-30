from app.models import Role

class RoleRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_by_id(self, role_id):
        return self.db_connector.session.execute(
            self.db_connector.select(Role).filter_by(id=role_id)
        ).scalar_one_or_none()

    def all(self):
        return self.db_connector.session.execute(
            self.db_connector.select(Role)
        ).scalars().all()
