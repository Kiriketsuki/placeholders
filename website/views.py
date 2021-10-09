from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from .helper import hasDigit, hasSpecialCharacters
from .models import User, building, Preference
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import sqlalchemy
import os
import pandas as pd
from dateutil import parser

views = Blueprint("views", __name__)

# Landing page
@views.route("/", methods=["GET", "POST"])
def landing():
    if request.method == "POST":
        # Get input from login form
        email = request.form.get("email")
        password = request.form.get("password")

        if email == None:
            flash('Email required.', category='error')
        elif password == None:
            flash('Password required.', category='error')

        # Check if credentials are valid
        # Check database for such user
        user = User.query.filter_by(email = email).first()
    
        # If user email exists
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully!', category='success')
                login_user(user, remember=True) # remember allows user to stay logged in
                return redirect(url_for('views.recommendations', logged_in=True))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("landing.html", user=current_user)

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
                login_user(newUser, remember=True) # remember allows user to stay logged in
                return redirect(url_for('views.recommendations'))
            except sqlalchemy.exc.IntegrityError:
                flash('Account already exists.', category='error')

    return render_template("sign_up.html", user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('views.landing'))

# TODO: implement this function
# Forgot password page
@views.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get('email')

        if email == None:
            flash('Email required.', category='error') 

        # Check if credentials are valid
        # Check database for such user
        user = User.query.filter_by(email = email).first()
    
        # If user email exists
        if not user:
            flash('Email does not exist.', category='error')
        else:
            # generate random new password
            # reset database with the new password
            # send email containing new password to user
            pass
        
    return render_template("forgot_pw.html")

# Homepage
@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/account/settings", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        thisUser = User.query.filter_by(id=current_user.get_id()).first()

        if request.form.get('firstName') == "" and request.form.get('lastName') == "" and request.form.get('email') == "" and request.form.get('password') == "":
            flash("Empty fields.", category='error')
        else:
            firstName = thisUser.firstName if request.form.get('firstName') == "" else request.form.get('firstName')
            lastName = thisUser.lastName if request.form.get('lastName') == "" else request.form.get('lastName')
            email = thisUser.email if request.form.get('email') == "" else request.form.get('email')

            # Check if credentials meet requirements
            if hasDigit(firstName):
                flash('First name must not contain numerical characters.', category='error')
            elif len(firstName) < 2:
                flash('First name is too short.', category='error')

            if hasDigit(lastName):
                flash('Last name must not contain numerical characters.', category='error')
            elif len(lastName) < 2:
                flash('Last name is too short.', category='error')

            if len(email) < 10 or "@" not in email:
                flash('Not a valid email.', category='error')

            if request.form.get('password') == "":
                pwChanged = False # Boolean var to check if pw changed. False -> pw not changed
                password = thisUser.password 
            else: 
                pwChanged = True # Boolean var to check if pw changed. True -> pw changed
                password = request.form.get('password')
                if len(password) < 8:
                    flash('Password too short.', category='error')
                elif not hasSpecialCharacters(password):
                    flash('Password must include at least one special character.', category='error')
                else:
                    # Update user profile
                    thisUser.firstName = firstName
                    thisUser.lastName = lastName
                    thisUser.email = email
                    thisUser.password = generate_password_hash(password, method = 'sha256') if pwChanged else password

                pwChanged = False # Reset
            
            db.session.commit()
            flash('Profile updated!', category='success')
            print(firstName, lastName, email, password)

        print("Submit")

    return render_template("profile.html", username = current_user)

@views.route("/account/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "POST":
        houseType = request.form.get('typeOfHouse')
        budget = request.form.get('budget')
        maritalStatus = request.form.get('maritalStatus')
        cpf = request.form.get('cpfSavings')
        ownCar = True if request.form.get('ownCar') == "Yes" else False
        amenities = request.form.getlist('amenities')
        preferredLocations = request.form.getlist('locations')

        print(houseType, budget, maritalStatus, cpf, ownCar, amenities, preferredLocations)

        newPreference = Preference(houseType= houseType, budget=budget, maritalStatus=maritalStatus, cpf=cpf, ownCar=ownCar, amenities=amenities, preferredLocations=preferredLocations, uid=current_user.get_id())

        db.session.add(newPreference)
        db.session.commit()

    return render_template("preferences.html", username = current_user)

@views.route("/go_to_home")
def home_redirect():
    return redirect(url_for("views.home"))

@views.route("/recommendations")
@login_required
def recommendations():
    admin = User.query.filter_by(firstName = "admin").first()
    return render_template("top_picks_logged_in.html", user=admin)

@views.route('/recommendations/guest')
def recommendations_guest():
    return render_template("top_picks_guest.html", user=current_user)

# TODO combine the top two into one (dont need! because recommendations require login and guest dosen't)
        
@views.route("/base_template")
def base_template():
    return render_template("base.html")

# @views.route("/results")
# def base_template():
#     render_template("base.html")

@views.route("/map")
def map():
    return render_template("map.html", user = current_user)

@views.route("/compare")
def compare():
    return render_template("compare.html")

@views.route("/results")
def results():
    return render_template("results.html")

@views.route("/csv")
def csv():
    return render_template("csv_chart.html", user = current_user)

@views.route("/jovians_debug")
def jovian():
    user = User.query.filter_by(firstName ="admin").first()
    for item in user.recommended:
        print(item.block)
    return f"{user.recommended[0].block}"

# !temp fix to add buildings into csv
@views.route("/import_buildings")
def import_buildings():
    file = "website/gov_data.csv"
    cwd = os.getcwd()
    data = pd.read_csv(os.path.normcase(os.path.join(cwd,file)))
    test = data.head(5) # adding only 5

    for index, row in test.iterrows():
        id = row['_id']
        month = parser.parse(row['month'])
        town = row['town']
        flat_type = row['flat_type']
        block = row['block']
        street_name = row['street_name']
        storey_range = row['storey_range']
        floor_area_sqm = row['floor_area_sqm']
        flat_model = row['flat_model']
        lease_commence_date = (row['lease_commence_date'])
        remaining_lease = row['remaining_lease']
        resale_price = row['resale_price']

        new_building = building(id = id, month = month, town = town, flat_type = flat_type, block = block, street_name = street_name, storey_range = storey_range, floor_area_sqm = floor_area_sqm, flat_model = flat_model, lease_commence_date = lease_commence_date, resale_price = resale_price, remaining_lease = remaining_lease)
        db.session.add(new_building)
        db.session.commit()
    return redirect(url_for('views.landing'))

@views.route("/create_admin")
def create_admin():
    admin = User(firstName = "admin", lastName = "supreme", email = "testing@gmail.com", password = generate_password_hash("password", method = 'sha256'))
    db.session.add(admin)
    db.session.commit()

    # I HAVENT TOOK CZ2007 IDK HOW TO DATABASE???
    # the above function imports 5 buildings so ill just add all 5 to my admin account
    # TODO something something select * from buildings something something add to user
    for i in range(1,6):
        temp_building = building.query.filter_by(id = i).first()
        temp_building.recommended_to.append(admin)
        db.session.commit()
    return redirect(url_for("views.landing"))

# ! does not work because I HAVENT LEARNT DATABASES HOW DO I SQL?????
@views.route("/testing_sql")
def testing_sql():
    for building in db.session.query("building"):
        print(building.block)