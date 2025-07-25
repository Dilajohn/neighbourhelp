from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Issue
from app import db
from functools import wraps
from flask import session

admin_routes = Blueprint("admin_routes", __name__, template_folder="../templates/admin")


# Decorator to protect admin routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access admin area.", "warning")
            return redirect(url_for("admin_auth.admin_login"))
        return f(*args, **kwargs)

    return decorated_function


@admin_routes.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    page = request.args.get("page", 1, type=int)
    issues = Issue.query.order_by(Issue.timestamp.desc()).paginate(
        page=page, per_page=5
    )
    return render_template("admin/dashboard.html", issues=issues)


@admin_routes.route("/admin/issue/<int:issue_id>")
@admin_required
def admin_view_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return render_template("admin/view_issue.html", issue=issue)


@admin_routes.route("/admin/issue/delete/<int:issue_id>", methods=["POST"])
@admin_required
def admin_delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    flash("Issue deleted successfully.", "success")
    return redirect(url_for("admin_routes.admin_dashboard"))
