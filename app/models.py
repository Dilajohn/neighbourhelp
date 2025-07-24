from datetime import datetime
from app import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# === Add to app/forms.py ===
from wtforms import PasswordField, BooleanField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='pending')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)