from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from .helper import hasDigit, hasSpecialCharacters
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import sqlalchemy

views = Blueprint("views", __name__)

# Landing page
@views.route("/", methods=["GET", "POST"])
def landing():
    if request.method == "POST":
        data = request.form
        print(data)
    return render_template("landing.html")

# Sign up page
@views.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form.get("first-name")
        lastName = request.form.get("last-name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")
        
        # Error checking
        if firstName == None:
            flash('First name cannot be empty.', category='error')
        else:
            if hasDigit(firstName):
                flash('First name must not contain numerical characters.', category='error')
            elif len(firstName) < 2:
                flash('First name is too short.', category='error')
        
        if lastName == None:
            flash('Last name cannot be empty.', category='error')
        else:
            if hasDigit(lastName):
                flash('Last name must not contain numerical characters.', category='error')
            elif len(lastName) < 2:
                flash('Last name is too short.', category='error')
        
        if len(email) < 10 or "@" not in email:
            flash('Not a valid email.', category='error')
        
        if len(password) < 8:
            flash('Password too short.', category='error')
        elif not hasSpecialCharacters(password):
            flash('Password must include at least one special character.', category='error')
        elif password != confirmPassword:
            flash('Passwords do not match.', category='error')
        else:
            # add user to DB
            newUser = User(firstName=firstName, lastName=lastName, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(newUser)

            # check if account already exists
            try:
                db.session.commit()
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            except sqlalchemy.exc.IntegrityError:
                flash('Account already exists.', category='error')

    return render_template("sign_up.html")

# Forgot password page
@views.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    return render_template("forgot_pw.html")

# Homepage
@views.route("/home")
def home():
    return render_template("home.html")

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

@views.route("/recommendations")
def recommendations():
    logged_in = True;
    if logged_in:
        return render_template("top_picks_logged_in.html")
    else:
        return render_template("top_picks_guest.html")
        
@views.route("/base_template")
def base_template():
    render_template("base.html")

# @views.route("/results")
# def base_template():
#     render_template("base.html")

@views.route("/map")
def map():
    render_template("map.html")

@views.route("/compare")
def compare():
    render_template("compare.html")
