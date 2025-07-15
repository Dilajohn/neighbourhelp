from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simple in-memory storage for demonstration
issues = []

def main():
    print("Welcome to NeighbourHelp!")

# Simple HTML form and list interface, no templates for brevity
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>NeighbourHelp - Report an Issue</title>
</head>
<body>
    <h1>Report a Community Issue</h1>
    <form method="post" action="/">
        <label for="description">Issue Description:</label><br>
        <textarea name="description" id="description" cols="30" rows="3" required></textarea><br><br>
        <label for="location">Location:</label><br>
        <input type="text" name="location" id="location" required><br><br>
        <button type="submit">Submit Report</button>
    </form>
    <h2>Reported Issues</h2>
    <ul>
        {% for issue in issues %}
            <li><strong>{{issue.location}}:</strong> {{issue.description}}</li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        desc = request.form["description"]
        loc = request.form["location"]
        issues.append({"description": desc, "location": loc})
    return render_template_string(HTML, issues=issues)

if __name__ == "__main__":
    app.run(debug=True)
