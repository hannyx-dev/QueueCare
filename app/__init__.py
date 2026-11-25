
from flask import Flask
from config import Config
from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    from app.auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from app.patients import patient
    app.register_blueprint(patient, url_prefix="/patient")

    return app
