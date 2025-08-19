from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Issue
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="../templates/admin")


# Dashboard (with pagination)
@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    page = request.args.get("page", 1, type=int)
    issues = Issue.query.order_by(Issue.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template("admin/dashboard.html", issues=issues)


# View Issue
@admin_bp.route("/issue/<int:issue_id>")
@login_required
def view_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return render_template("admin/view_issue.html", issue=issue)


# Resolve Issue
@admin_bp.route("/issue/<int:issue_id>/resolve", methods=["POST"])
@login_required
def resolve_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    issue.status = "Resolved"
    db.session.commit()
    flash(f"Issue '{issue.title}' marked as resolved.", "success")
    return redirect(url_for("admin.admin_dashboard"))


# Delete Issue
@admin_bp.route("/issue/<int:issue_id>/delete", methods=["POST"])
@login_required
def delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    flash("Issue deleted successfully!", "success")
    return redirect(url_for("admin.admin_dashboard"))


# Edit Issue
@admin_bp.route("/issue/<int:issue_id>/edit", methods=["GET", "POST"])
@login_required
def edit_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)

    if request.method == "POST":
        issue.title = request.form["title"]
        issue.description = request.form["description"]
        issue.location = request.form["location"]
        issue.category = request.form["category"]
        issue.status = request.form["status"]

        # Handle image upload
        if "image_file" in request.files:
            file = request.files["image_file"]
            if file and file.filename.strip():
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, "static/uploads", filename)
                file.save(upload_path)
                issue.image_filename = filename

        db.session.commit()
        flash("Issue updated successfully!", "success")
        return redirect(url_for("admin.view_issue", issue_id=issue.id))

    return render_template("admin/edit_issue.html", issue=issue)
