from flask import Blueprint, render_template

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def index():
    return "<h1>Welcome to NeighbourHelp</h1><p><a href='/admin/dashboard'>Go to Admin Dashboard</a></p>"
