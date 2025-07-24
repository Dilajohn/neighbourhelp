import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Issue, Admin
from app.forms import IssueForm, LoginForm

bp = Blueprint("main", __name__)  # registered in __init__.py


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.admin_dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.admin_dashboard"))
        else:
            flash("Login failed. Check username/password.", "danger")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


@bp.route("/admin")
@login_required
def admin_dashboard():
    issues = Issue.query.order_by(Issue.date_posted.desc()).all()
    return render_template("admin_dashboard.html", issues=issues)


@bp.route("/")
def index():
    issues = Issue.query.order_by(Issue.date_posted.desc()).all()
    return render_template("index.html", issues=issues)


@bp.route("/report", methods=["GET", "POST"])
def report():
    form = IssueForm()
    if form.validate_on_submit():
        filename = None
        if form.image_file.data:
            filename = secure_filename(form.image_file.data.filename)
            filepath = os.path.join("app/static/uploads", filename)
            form.image_file.data.save(filepath)

        new_issue = Issue(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            category=form.category.data,
            image_file=filename,
        )
        db.session.add(new_issue)
        db.session.commit()
        flash("Issue reported successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("report_issue.html", form=form)
