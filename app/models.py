# app/models.py
import datetime
from flask_login import UserMixin
from app import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='pending')
    date_posted = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

