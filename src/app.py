from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simple in-memory storage for demonstration
issues = []

# HTML templates as strings

WELCOME_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>NeighbourHelp - Welcome</title>
</head>
<body>
    <h1>Welcome to NeighbourHelp</h1>
    <p><a href="{{ url_for('report_issue') }}">Report a Community Issue</a></p>
</body>
</html>
'''

REPORT_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>NeighbourHelp - Report an Issue</title>
</head>
<body>
    <h1>Report a Community Issue</h1>
    <form method="post" action="{{ url_for('report_issue') }}">
        <label for="description">Issue Description:</label><br>
        <textarea name="description" id="description" cols="30" rows="3" required></textarea><br><br>
        <label for="location">Location:</label><br>
        <input type="text" name="location" id="location" required><br><br>
        <button type="submit">Submit Report</button>
    </form>
    <h2>Reported Issues</h2>
    <ul>
        {% for issue in issues %}
            <li><strong>{{ issue.location }}:</strong> {{ issue.description }}</li>
        {% else %}
            <li>No issues reported yet.</li>
        {% endfor %}
    </ul>
    <p><a href="{{ url_for('home') }}">Back to Home</a></p>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(WELCOME_HTML)

@app.route("/report", methods=["GET", "POST"])
def report_issue():
    if request.method == "POST":
        desc = request.form["description"]
        loc = request.form["location"]
        issues.append({"description": desc, "location": loc})
        # Redirect to GET after POST to avoid form resubmission on refresh
        return redirect(url_for('report_issue'))
    return render_template_string(REPORT_HTML, issues=issues)

if __name__ == "__main__":
    app.run(debug=True)

