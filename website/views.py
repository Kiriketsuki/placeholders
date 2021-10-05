from flask import Blueprint
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/base_template")
def base_template():
    render_template("base.html")

@views.route("/profile")
def profile():
    args = request.args
    username = args.get('username')
    return render_template("index.html", username = username)

@views.route("/go_to_home")
def home_redirect():
    return redirect(url_for("views.home"))

@views.route("/recommendations")
def recommendations():
    logged_in = True;
    if not logged_in:
        return render_template("top_picks_logged_in.html")
    else:
        return render_template("top_picks_guest.html")
        