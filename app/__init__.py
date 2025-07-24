from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from datetime import datetime


# Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


# Login settings
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Import models for user loader setup
    from app.models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Register Blueprints

    from app.routes.admin import admin_routes
    from app.routes.admin_auth import admin_auth

    app.register_blueprint(admin_routes)
    app.register_blueprint(admin_auth)

    @app.context_processor
    def inject_now():
        return {"current_year": datetime.datetime.now(datetime.timezone.utc).year}

    return app
