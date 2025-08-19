from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import Admin
from app.forms import AdminLoginForm

admin_auth_bp = Blueprint("admin_auth", __name__, url_prefix="/admin", template_folder="../templates/admin")

@admin_auth_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin.admin_dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("admin/login.html", form=form)

@admin_auth_bp.route("/logout", methods=["POST"])
def admin_logout():
    if current_user.is_authenticated:
        logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("admin_auth.admin_login"))


