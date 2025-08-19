from app import db
from flask_login import UserMixin
from datetime import datetime


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed password

    def __repr__(self):
        return f"<Admin {self.username}>"


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default="Pending")  # Pending, In Progress, Resolved
    image_filename = db.Column(db.String(255), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Issue {self.title}>"
