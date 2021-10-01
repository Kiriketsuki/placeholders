from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from helper import hasDigit, hasSpecialCharacters

views = Blueprint(__name__, "views")

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
        print(firstName, lastName)
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
            flash('Account created!', category='success')
            #add user to DB

    return render_template("sign_up.html")

# Forgot password page
@views.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    return render_template("forgot_pw.html")

@views.route("/profile")
def profile():
    args = request.args
    username = args.get('username')
    return render_template("index.html", username = username)

@views.route("/go_to_home")
def home_redirect():
    return redirect(url_for("views.home"))

@views.route("/base_template")
def base_template():
    render_template("base.html")

