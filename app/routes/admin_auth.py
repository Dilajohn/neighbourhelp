from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Admin
from app.forms import AdminLoginForm

admin_auth_bp = Blueprint(
    "admin_auth",
    __name__,
    url_prefix="/admin",
    template_folder="../templates/admin"
)

# Admin login
@admin_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash("Login successful!", "success")
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("admin/login.html", form=form)

# Admin logout
@admin_auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin_auth.login"))

