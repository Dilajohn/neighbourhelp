from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models import Admin
from app.forms import AdminLoginForm
from app import db

admin_auth = Blueprint("admin_auth", __name__, template_folder="../templates/admin")


@admin_auth.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            # Set session for logged-in admin
            session["admin_logged_in"] = True
            flash("Logged in successfully.", "success")

            # Redirect to the correct dashboard route
            return redirect(url_for("admin_routes.admin_dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html", form=form)


@admin_auth.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("admin_auth.admin_login"))

