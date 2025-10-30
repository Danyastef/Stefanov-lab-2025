import os

from flask import Flask, session, request
from flask_login import current_user
from flask_migrate import Migrate

from app.models import db, VisitLog

migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import auth
    app.register_blueprint(auth.bp)
    auth.login_manager.init_app(app)

    from . import users
    app.register_blueprint(users.bp)
    app.route('/', endpoint='index')(users.index)

    from . import task
    app.register_blueprint(task.bp)

    from . import reports
    app.register_blueprint(reports.bp)

    @app.before_request
    def log_visit():
        if app.config.get('TESTING'):
            return

        ignored_paths = ('/static/', '/favicon.ico')
        if any(request.path.startswith(p) for p in ignored_paths):
            return

        from app.models import db
        log = VisitLog(
            path=request.path,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(log)
        db.session.commit()

    app.context_processor(lambda: {'can_user': auth.can_user})

    return app