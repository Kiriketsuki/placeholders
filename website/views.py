from flask import Blueprint
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("landing.html")

@views.route("/forgot_password")
def forgot_password():
    return render_template("forgot_pw.html")

@views.route("/signup")
def signup():
    return render_template("sign_up.html")

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

