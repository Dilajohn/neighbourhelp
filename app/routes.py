from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

main_bp = Blueprint('main', __name__)

# In-memory 'issues' store for demo purposes. For production, replace with DB storage.
issues = []

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        desc = request.form["description"]
        loc = request.form["location"]
        issues.append({"description": desc, "location": loc})
        return redirect(url_for('main.report'))
    return render_template("report.html", issues=issues)
