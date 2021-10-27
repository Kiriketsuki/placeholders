import json

from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.event import listen

from . import db

# association table for recommendations
recommendations = db.Table(
    "recommendations", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("building_id", db.Integer, db.ForeignKey("building.id")),
)

# association table for favourites
favourites = db.Table(
    "favourites", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("building_id", db.Integer, db.ForeignKey("building.id")),
)

class Recommendation(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, primary_key=True)
    amenities_type = db.Column(db.String(150))
    amenities_list = db.Column(db.JSON)
    num_amenities = db.Column(db.Integer)
    distance_from_target = db.Column(db.String(150), nullable=True)

    # nearby_amenities = db.Column(db.JSON)

# User schema
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    photo = db.Column(db.String(150), default = "assets/user_photo/default.jpg")
    recommended = db.relationship(
        "building",
        secondary=recommendations,
        backref=db.backref("recommended_to", lazy="dynamic"),
    )
    favourites = db.relationship(
        "building",
        secondary=favourites,
        backref=db.backref("favourited_by", lazy="dynamic"),
    )

    is_guest = db.Column(db.Boolean, default = False) # to make everything can be based on sidebar.html

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseType = db.Column(db.String(150))
    budget = db.Column(db.String(150))
    # monthlyIncome = db.Column(db.String(150))
    # maritalStatus = db.Column(db.String(150))
    # cpf = db.Column(db.String(150))
    # ownCar = db.Column(db.Boolean)
    amenities = db.Column(db.JSON)
    distance = db.Column(db.Integer)
    preferredLocations = db.Column(db.JSON)
    uid = db.Column(db.Integer,
                    db.ForeignKey("user.id"),
                    unique=True,
                    nullable=True)


# building schema
class building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    month = db.Column(db.DateTime)
    town = db.Column(db.String(150))
    flat_type = db.Column(db.String(150))
    block = db.Column(db.String(150))
    street_name = db.Column(db.String(150))
    storey_range = db.Column(db.String(150))
    floor_area_sqm = db.Column(db.Float)
    flat_model = db.Column(db.String(150))
    lease_commence_date = db.Column(db.Integer)
    remaining_lease = db.Column(db.String(150))
    resale_price = db.Column(db.Float)
    image_path = db.Column(db.String(150))
    contact = db.Column(db.String(150))

