from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from app.models import Issue
from app import db
from functools import wraps
import os
from werkzeug.utils import secure_filename
from app.forms import IssueForm

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
    page = request.args.get('page', 1, type=int)
    issues = Issue.query.order_by(Issue.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template("dashboard.html", issues=issues)


@admin_routes.route("/admin/issue/<int:issue_id>")
@admin_required
def admin_view_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return render_template("view_issue.html", issue=issue)


@admin_routes.route("/admin/resolve/<int:issue_id>")
@admin_required
def resolve_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    issue.status = "resolved"
    db.session.commit()
    flash(f"Issue '{issue.title}' marked as resolved.", "success")
    return redirect(url_for("admin_routes.admin_dashboard"))


@admin_routes.route("/admin/issue/delete/<int:issue_id>", methods=["POST"])
@admin_required
def admin_delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    flash("Issue deleted successfully.", "success")
    return redirect(url_for("admin_routes.admin_dashboard"))


@admin_routes.route("/admin/issue/edit/<int:issue_id>", methods=["GET", "POST"])
@admin_required
def edit_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = IssueForm(obj=issue)  # pre-populates form with current issue data

    if form.validate_on_submit():
        issue.title = form.title.data
        issue.description = form.description.data
        issue.location = form.location.data
        issue.category = form.category.data
        issue.status = form.status.data

        # Handle image upload
        if form.image_file.data:
            filename = secure_filename(form.image_file.data.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image_file.data.save(upload_path)
            issue.image_filename = filename

        db.session.commit()
        flash("Issue updated successfully.", "success")
        return redirect(url_for("admin_routes.admin_view_issue", issue_id=issue.id))

    return render_template("edit_issue.html", form=form, issue=issue)
