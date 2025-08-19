from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "admin_auth.admin_login"
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Blueprints
    from app.routes.admin import admin_bp
    from app.routes.admin_auth import admin_auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_auth_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_now():
        return {"current_year": datetime.now().year}

    return app
