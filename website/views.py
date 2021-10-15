from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy.orm import query
from .helper import hasDigit, hasSpecialCharacters
from .models import User, building
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import sqlalchemy
import os
import pandas as pd
from dateutil import parser

views = Blueprint("views", __name__)


##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
#####################################################! HTML RENDERERS ####################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

# Landing page
@views.route("/", methods=["GET", "POST"])
def landing():
    init_db()

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
                return redirect(url_for('views.preferences', logged_in=True))
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
        # elif not hasSpecialCharacters(password):
        #     flash('Password must include at least one special character.', category='error')
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
                # login_user(newUser, remember=True) # remember allows user to stay logged in
                return redirect(url_for('views.landing'))
            except sqlalchemy.exc.IntegrityError:
                flash('Account already exists.', category='error')

    return render_template("sign_up.html", user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('views.landing'))


# Forgot password page
@views.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.POST.get('email')

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

@views.route("/submit_preferences", methods = ["GET", "POST"])
def submit_preferences():
    return render_template("submit_preferences.html", user = current_user)

@views.route("/update_preferences", methods = ["GET", "POST"])
@login_required
def update_preferences():
    return render_template("update_preferences.html", user = current_user)

@views.route("/account")
def profile():
    return render_template("profile.html", user = current_user)

@views.route("/account/preferences")
def preferences():
    return render_template("preferences.html", user = current_user)

@views.route("/go_to_home")
def home_redirect():
    return redirect(url_for("views.home"))

@views.route("/recommendations")
def recommendations():
    if current_user.is_authenticated:
        return render_template("top_picks_logged_in.html", user = current_user)
    else:
        return render_template("top_picks_guest.html", user = current_user)

# @views.route('/recommendations/guest')
# def recommendations_guest():
#     return render_template("top_picks_guest.html", user = current_user)

# TODO combine the top two into one
        
@views.route("/base_template")
def base_template():
    return render_template("base.html",user = current_user)


@views.route("/map")
def map():
    return render_template("map.html", user = current_user)

@views.route("/compare")
def compare():
    return render_template("compare.html", user = current_user)

@views.route("/testing")
def testing():
    return render_template("testing.html")

@views.route("/sidebar")
def sidebar():
    return render_template("sidebar.html")

@views.route("/csv")
def csv():
    return render_template("csv_chart.html", user = current_user)



##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
#####################################################! HELPER FUNCTIONS ##################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
def import_buildings():
    file = "website/gov_data.csv"
    cwd = os.getcwd()
    data = pd.read_csv(os.path.normcase(os.path.join(cwd,file)))
    test = data.head(5) # adding only 5

    # read from dataframe, create building, commit to db
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
        image_path = row['image_path']

        new_building = building(id = id, month = month, town = town, flat_type = flat_type, block = block, street_name = street_name, storey_range = storey_range, floor_area_sqm = floor_area_sqm, flat_model = flat_model, lease_commence_date = lease_commence_date, resale_price = resale_price, remaining_lease = remaining_lease, image_path = image_path)
        db.session.add(new_building)
        db.session.commit()

def create_admin():
    from werkzeug.security import generate_password_hash
    admin = User(firstName = "admin", lastName = "supreme", email = "testing@gmail.com", password = generate_password_hash("password", method = 'sha256'))
    db.session.add(admin)
    db.session.commit()
    # I HAVENT TOOK CZ2007 IDK HOW TO DATABASE???
    # the above function imports 5 buildings so ill just add all 5 to my admin account
    for i in range(1,6):
        temp_building = building.query.filter_by(id = i).first()
        temp_building.recommended_to.append(admin)
        db.session.commit()
    return redirect(url_for("views.landing"))

def init_db():
    if db.session.query(User).count() == 0:
        import_buildings()
        create_admin()

@views.route("/jovians_debug")
def jovian():
    user = User.query.filter_by(firstName ="admin").first()

    return render_template("top_picks_logged_in.html", user = user)