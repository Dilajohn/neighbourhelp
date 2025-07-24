from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import Admin
from app.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.admin_dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if not username or not password or not password_confirm:
            flash("Please fill out all fields.", "warning")
        elif password != password_confirm:
            flash("Passwords do not match.", "warning")
        elif Admin.query.filter_by(username=username).first():
            flash("Username already exists.", "warning")
        else:
            new_user = Admin(
                username=username, password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created! You can now log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")
