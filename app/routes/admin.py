from flask import Blueprint, render_template, session, redirect, url_for

admin_routes = Blueprint("admin", __name__, template_folder="../templates/admin")


@admin_routes.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_auth.admin_login"))
    # Logic to fetch data for the dashboard can be added here
    # For now, we will just render a placeholder template
    return render_template("dashboard.html")  # Create this next
