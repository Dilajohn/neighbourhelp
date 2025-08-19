import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Issue
from app.forms import IssueForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    issues = Issue.query.order_by(Issue.date_posted.desc()).all()
    return render_template("index.html", issues=issues)

@main_bp.route("/report", methods=["GET", "POST"])
def report():
    form = IssueForm()
    if form.validate_on_submit():
        filename = None
        if form.image_file.data:
            filename = secure_filename(form.image_file.data.filename)
            upload_dir = current_app.config.get("UPLOAD_FOLDER")
            os.makedirs(upload_dir, exist_ok=True)
            form.image_file.data.save(os.path.join(upload_dir, filename))

        new_issue = Issue(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            category=form.category.data,
            status=form.status.data,              # 'open' | 'in_progress' | 'resolved'
            image_filename=filename,              # NOTE: image_filename
        )
        db.session.add(new_issue)
        db.session.commit()
        flash("Issue reported successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("report_issue.html", form=form)
