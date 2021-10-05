from flask import Blueprint
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/base_template")
def base_template():
    render_template("base.html")

@views.route("/account/settings")
def profile():
    args = request.args
    username = args.get('username')
    return render_template("profile.html", username = username)

@views.route("/account/preferences")
def preferences():
    args = request.args
    username = args.get('username')
    return render_template("preferences.html", username = username)

@views.route("/go_to_home")
def home_redirect():
    return redirect(url_for("views.home"))