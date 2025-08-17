from app import create_app, db
from app.models import Admin

app = create_app()

with app.app_context():
    # Drop & recreate tables if needed (be careful with drop_all in production!)
    db.drop_all()
    db.create_all()

    # Create default admin if not exists
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin", email="admin@example.com")
        admin.set_password("admin123")  # change this later
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created: admin / admin123")
    else:
        print("ℹ️ Admin already exists.")
