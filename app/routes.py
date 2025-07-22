import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import db
from app.models import Issue
from app.forms import IssueForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    issues = Issue.query.order_by(Issue.date_posted.desc()).all()
    return render_template('index.html', issues=issues)

@bp.route('/report', methods=['GET', 'POST'])
def report():
    form = IssueForm()
    if form.validate_on_submit():
        filename = None
        if form.image_file.data:
            filename = secure_filename(form.image_file.data.filename)
            filepath = os.path.join('app/static/uploads', filename)
            form.image_file.data.save(filepath)

        new_issue = Issue(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            category=form.category.data,
            image_file=filename
        )
        db.session.add(new_issue)
        db.session.commit()
        flash('Issue reported successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('report_issue.html', form=form)