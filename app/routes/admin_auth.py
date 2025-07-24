from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models import Admin
from app import db
from werkzeug.security import check_password_hash

admin_auth = Blueprint("admin_auth", __name__, template_folder="../templates/admin")


@admin_auth.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session["admin_logged_in"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@admin_auth.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("admin_auth.admin_login"))
