from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Issue

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Dashboard
@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    issues = Issue.query.order_by(Issue.date_posted.desc()).all()
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
    flash("Issue marked as resolved!", "success")
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


# ✨ NEW: Edit Issue
@admin_bp.route("/issue/<int:issue_id>/edit", methods=["GET", "POST"])
@login_required
def edit_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)

    if request.method == "POST":
        issue.title = request.form["title"]
        issue.description = request.form["description"]
        issue.location = request.form["location"]
        issue.category = request.form["category"]

        # Handle image update (optional)
        if "image_filename" in request.files:
            file = request.files["image_filename"]
            if file and file.filename.strip():
                # simple: store filename only
                issue.image_filename = file.filename
                # if you want file saving: file.save(os.path.join(UPLOAD_FOLDER, file.filename))

        db.session.commit()
        flash("Issue updated successfully!", "success")
        return redirect(url_for("admin.view_issue", issue_id=issue.id))

    return render_template("admin/edit_issue.html", issue=issue)

