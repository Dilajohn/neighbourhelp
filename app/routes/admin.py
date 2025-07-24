from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models import Issue
from app import db

admin_routes = Blueprint("admin", __name__)


@admin_routes.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_auth.admin_login"))

    page = request.args.get("page", 1, type=int)
    issues = Issue.query.order_by(Issue.timestamp.desc()).paginate(
        page=page, per_page=5
    )
    return render_template("admin/dashboard.html", issues=issues)


@admin_routes.route("/admin/issue/<int:issue_id>")
def view_issue(issue_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_auth.admin_login"))

    issue = Issue.query.get_or_404(issue_id)
    return render_template("admin/view_issue.html", issue=issue)


@admin_routes.route("/admin/issue/<int:issue_id>/resolve")
def resolve_issue(issue_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_auth.admin_login"))

    issue = Issue.query.get_or_404(issue_id)
    issue.status = "resolved"
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))


@admin_routes.route("/admin/issue/<int:issue_id>/delete", methods=["POST"])
def delete_issue(issue_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_auth.admin_login"))

    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))
