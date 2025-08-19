from app import db
from app.models import Admin

if not Admin.query.filter_by(username="admin").first():
    admin = Admin(username="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created: admin / admin123")
else:
    print("ℹ️ Admin already exists.")