import os

import pandas as pd
import sqlalchemy
from dateutil import parser
from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from . import db
from .helper import hasDigit
from .helper import hasSpecialCharacters
from .models import building
from .models import Preference
from .models import User

import random
import json
from sqlalchemy import func

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

    if request.method == "POST":
        # Get input from login form
        email = request.form.get("email")
        password = request.form.get("password")

        if email == None:
            flash("Email required.", category="error")
        elif password == None:
            flash("Password required.", category="error")

        # Check if credentials are valid
        # Check database for such user
        user = User.query.filter_by(email=email).first()

        # If user email exists
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                # remember allows user to stay logged in
                login_user(user, remember=True)
                return redirect(
                    url_for("views.home", logged_in=True))
            else:
                flash("Incorrect password, please try again.",
                      category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("landing.html", user=current_user)


@views.route("/guest_creation", methods=["GET", "POST"])
def create_guest():

    number_gen = len(User.query.order_by(User.id).all())
    random.seed(number_gen)
    email = str(random.random())

    temp_user = User(
        firstName="guest",
        lastName="",
        email=email,
        password=generate_password_hash("", method="sha256"),
        is_guest=True
    )

    db.session.add(temp_user)
    db.session.commit()
    guest = json.dumps(email, default=lambda x: list(x)
                       if isinstance(x, set) else x)
    login_user(temp_user, remember=False)
    return redirect(url_for("views.home", user=guest))


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
            flash("First name cannot be empty.", category="error")
        else:
            if hasDigit(firstName):
                flash(
                    "First name must not contain numerical characters.",
                    category="error",
                )
            elif len(firstName) < 2:
                flash("First name is too short.", category="error")

        if lastName == None:
            flash("Last name cannot be empty.", category="error")
        else:
            if hasDigit(lastName):
                flash("Last name must not contain numerical characters.",
                      category="error")
            elif len(lastName) < 2:
                flash("Last name is too short.", category="error")

        if len(email) < 10 or "@" not in email:
            flash("Not a valid email.", category="error")

        if len(password) < 8:
            flash("Password too short.", category="error")
        elif not hasSpecialCharacters(password):
            flash(
                "Password must include at least one special character.",
                category="error",
            )
        elif password != confirmPassword:
            flash("Passwords do not match.", category="error")
        else:
            # add user to DB
            newUser = User(
                firstName=firstName,
                lastName=lastName,
                email=email,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(newUser)

            # check if account already exists
            try:
                db.session.commit()
                flash("Account created!", category="success")
                # login_user(newUser, remember=True) # remember allows user to stay logged in
                return redirect(url_for("views.home"))
            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                flash("Account already exists.", category="error")

    return render_template("sign_up.html", user=current_user)


# login page
@views.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == None:
            flash("Email required.", category="error")
        elif password == None:
            flash("Password required.", category="error")

        # Check if credentials are valid
        # Check database for such user
        user = User.query.filter_by(email=email).first()

        # If user email exists
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                # remember allows user to stay logged in
                login_user(user, remember=True)
                return redirect(
                    url_for("views.home", logged_in=True))
            else:
                flash("Incorrect password, please try again.",
                      category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html")
# Logout user


@views.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for("views.landing"))

# Forgot password page


@views.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.POST.get("email")

        if email == None:
            flash("Email required.", category="error")

        # Check if credentials are valid
        # Check database for such user
        user = User.query.filter_by(email=email).first()

        # If user email exists
        if not user:
            flash("Email does not exist.", category="error")
        else:
            # generate random new password
            # reset database with the new password
            # send email containing new password to user
            pass

    return render_template("forgot_pw.html")


@views.route("/account/settings", methods=["POST", "GET"])
@login_required
def account_settings():
    if request.method == "POST":
        thisUser = User.query.filter_by(id=current_user.get_id()).first()

        if (request.form.get("firstName") == ""
                and request.form.get("lastName") == ""
                and request.form.get("email") == ""
                and request.form.get("password") == ""):
            flash("Empty fields.", category="error")
        else:
            firstName = (thisUser.firstName if request.form.get("firstName")
                         == "" else request.form.get("firstName"))
            lastName = (thisUser.lastName if request.form.get("lastName") == ""
                        else request.form.get("lastName"))
            email = (thisUser.email if request.form.get("email") == "" else
                     request.form.get("email"))

            # Check if credentials meet requirements
            if hasDigit(firstName):
                flash(
                    "First name must not contain numerical characters.",
                    category="error",
                )
            elif len(firstName) < 2:
                flash("First name is too short.", category="error")

            if hasDigit(lastName):
                flash("Last name must not contain numerical characters.",
                      category="error")
            elif len(lastName) < 2:
                flash("Last name is too short.", category="error")

            if len(email) < 10 or "@" not in email:
                flash("Not a valid email.", category="error")

            if request.form.get("password") == "":
                pwChanged = (
                    False  # Boolean var to check if pw changed. False -> pw not changed
                )
                thisUser.password = thisUser.password
            else:
                pwChanged = (
                    True  # Boolean var to check if pw changed. True -> pw changed
                )
                password = request.form.get("password")
                if len(password) < 8:
                    flash("Password too short.", category="error")
                elif not hasSpecialCharacters(password):
                    flash(
                        "Password must include at least one special character.",
                        category="error",
                    )
                else:
                    # Update user profile
                    thisUser.password = (generate_password_hash(
                        password, method="sha256") if pwChanged else password)

            thisUser.firstName = firstName
            thisUser.lastName = lastName
            thisUser.email = email

            print(firstName, lastName, email, pwChanged)  # DEBUGGING

            pwChanged = False  # Reset

            db.session.commit()

            flash("Profile updated!", category="success")

        print("Submit")

    return render_template("profile_settings.html", user=current_user)


@views.route("/account/")
def profile():
    return render_template("profile.html", user=current_user)


@views.route("/account/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "POST":
        # Check if db has user preference already
        # db cannot hold 2 preferences under same uid as it is unique
        # if preference does not exist for user then add normally
        # else update db row for particular uid
        print(current_user)  # DEBUGGING

        thisPreference = Preference.query.filter_by(
            id=current_user.get_id()).first()
        print(thisPreference)  # DEBUGGING

        attributes = {
            "houseType": None,
            "budget": None,
            "monthlyIncome": None,
            "maritalStatus": None,
            "cpf": None,
            "ownCar": None,
            "amenities": None,
            "preferredLocations": None,
        }

        attributes["houseType"] = request.form.get("typeOfHouse")
        attributes["budget"] = request.form.get("budget")
        attributes["monthlyIncome"] = request.form.get("monthlyIncome")
        attributes["maritalStatus"] = request.form.get("maritalStatus")
        attributes["cpf"] = request.form.get("cpfSavings")
        attributes["ownCar"] = True if request.form.get(
            "ownCar") == "Yes" else False
        attributes["amenities"] = request.form.getlist("amenities")
        attributes["preferredLocations"] = request.form.getlist("locations")

        if None in attributes.values():
            flash("Empty fields. All fields must be filled in.",
                  category="error")
        else:
            if (thisPreference == None
                ):  # currently does not have preference hence can add to db
                newPreference = Preference(
                    houseType=attributes["houseType"],
                    budget=attributes["budget"],
                    monthlyIncome=attributes["monthlyIncome"],
                    maritalStatus=attributes["maritalStatus"],
                    cpf=attributes["cpf"],
                    ownCar=attributes["ownCar"],
                    amenities=attributes["amenities"],
                    preferredLocations=attributes["preferredLocations"],
                    uid=current_user.get_id(),
                )
                db.session.add(newPreference)
            else:  # has existing preference hence update row
                thisPreference.houseType = attributes["houseType"]
                thisPreference.budget = attributes["budget"]
                thisPreference.monthlyIncome = attributes["monthlyIncome"]
                thisPreference.maritalStatus = attributes["maritalStatus"]
                thisPreference.cpf = attributes["cpf"]
                thisPreference.ownCar = attributes["ownCar"]
                thisPreference.amenities = attributes["amenities"]
                thisPreference.preferredLocations = attributes[
                    "preferredLocations"]

            flash("Preferences updated!", category="success")

        print(
            attributes["houseType"],
            attributes["budget"],
            attributes["maritalStatus"],
            attributes["cpf"],
            attributes["ownCar"],
            attributes["amenities"],
            attributes["preferredLocations"],
        )  # DEBUGGING

        db.session.commit()

    return render_template("preferences.html", user=current_user)


@views.route("/home")
def home():
    list_of_favourited_buildings = sorted(db.session.query(building.id, func.count(
        User.id)).join(building.favourited_by).group_by(building.id).all(), key=lambda x: x[1])
    first_ten = list_of_favourited_buildings[:10]
    flag = False
    args = request.args
    try:
        email = args['email']
        print(email)
        guest = User.query.filter_by(email=email).first()
        flag = True
    except:
        pass

    print(args)
    # convert from list of numbers into list of buildings
    to_return = []
    for i in first_ten:
        building_id = i[0]
        temp_building = building.query.filter_by(id=building_id).first()
        to_return.append(temp_building)

    if not flag:
        return render_template("most_liked.html", user=current_user, to_display=to_return)
    else:
        print(guest)
        return render_template("most_liked.html", user=guest, to_display=to_return)

# to calculate results


@views.route("/calc")
def to_recommend():
    return render_template("calc_reco.html", user=current_user)

# to show results


@views.route("/recommended")
def recommended():
    if current_user.is_authenticated:
        return render_template("recommended.html", user=current_user)
    else:
        guest = User.query.filter_by(firstName="guest").first()
        return render_template("recommended.html", user=guest)

# to add favourites


@views.route("/add_favourites", methods=["POST"])
def add_favourites():
    building_id = json.loads(request.data)
    building_id = building_id['building_id']
    temp_building = building.query.filter_by(id=building_id).first()
    temp_building.favourited_by.append(current_user)
    db.session.commit()
    return jsonify({})

# view favourites


@views.route("/account/favourites")
def view_favourites():
    if not current_user.is_guest:
        return render_template("favourites.html", user=current_user)


@views.route("/compare")
@login_required
def compare():
    return render_template("compare.html", user=current_user)


@views.route("/csv")
def csv():
    return render_template("csv_chart.html", user=current_user)


##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
#####################################################! HELPER FUNCTIONS ##################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
@views.route("/jovians_debug")
def jovian():
    # # ! get list of buildings and how many favourites they have
    # fav_buildings = db.session.query(building.id, func.count(User.id)).join(building.favourited_by).group_by(building.id).all()

    # # ! get list of users and how many favourites they have
    # fav_users = db.session.query(User.id, func.count(building.id)).join(User.favourites).group_by(User.id).all()

    # print(fav_buildings)
    # print(fav_users)

    return ("o")


# get admin function for debug
def get_admin():
    if not current_user.is_authenticated():
        return User.query.filter_by(firstName="admin").first()


@views.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0
