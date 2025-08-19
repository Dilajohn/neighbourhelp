import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "devkey"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(basedir, 'instance', 'site.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")

# Ensure folders exist
os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)
os.makedirs(os.path.join(basedir, "app", "static", "uploads"), exist_ok=True)
