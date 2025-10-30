from collections import namedtuple

class RoleRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_by_id(self, role_id):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("SELECT * FROM roles WHERE id = %s;", (role_id,))
            role = cursor.fetchone()
            if role:
                columns = [col[0] for col in cursor.description]
                RoleTuple = namedtuple('RoleTuple', columns)
                return RoleTuple(*role)
        return None
    
    def all(self):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("SELECT roles.* FROM roles")
            roles = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            RoleTuple = namedtuple('RoleTuple', columns)
            roles = [RoleTuple(*row) for row in roles]
        return roles