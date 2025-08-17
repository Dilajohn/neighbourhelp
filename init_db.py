# init_db.py
import os
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

# Create app using your factory
app = create_app()

with app.app_context():
    # Ensure instance folder exists
    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)

    # Create database tables
    db.create_all()
    print("✅ Database tables created")

    # Add default admin user (only if not exists)
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created (username: admin | password: admin123)")
    else:
        print("ℹ️ Admin user already exists, skipping...")
