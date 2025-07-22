from datetime import datetime
from app import db

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='pending')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)