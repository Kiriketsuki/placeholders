from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import json

from . import db

# association table
recommendations = db.Table(
    "recommendations",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("building_id", db.Integer, db.ForeignKey("building.id")),
)

# User schema


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    recommended = db.relationship(
        "building",
        secondary=recommendations,
        backref=db.backref("recommended_to", lazy="dynamic"),
    )
    pid = db.relationship("Preference", backref="user", uselist=False)

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.email


class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseType = db.Column(db.String(150))
    budget = db.Column(db.String(150))
    monthlyIncome = db.Column(db.String(150))
    maritalStatus = db.Column(db.String(150))
    cpf = db.Column(db.String(150))
    ownCar = db.Column(db.Boolean)
    amenities = db.Column(db.JSON)
    preferredLocations = db.Column(db.JSON)
    uid = db.Column(db.Integer,
                    db.ForeignKey("user.id"),
                    unique=True,
                    nullable=True)


# building schema


class building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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


# def create_admin():
#     from werkzeug.security import generate_password_hash
#     admin = User(firstName = "admin", lastName = "supreme", email = "testing@gmail.com", password = generate_password_hash("password", method = 'sha256'))
#     db.session.add(admin)
#     db.session.commit()
# event.listen(User.__table__, 'after_create', create_admin)

# @event.listens_for(building.__table__, 'after_create')
# def import_buildings():
#     import os
#     import pandas as pd
#     from dateutil import parser

#     file = "website/gov_data.csv"
#     cwd = os.getcwd()
#     data = pd.read_csv(os.path.normcase(os.path.join(cwd,file)))
#     test = data.head(5) # adding only 5

#     # read from dataframe, create building, commit to db
#     for index, row in test.iterrows():
#         id = row['_id']
#         month = parser.parse(row['month'])
#         town = row['town']
#         flat_type = row['flat_type']
#         block = row['block']
#         street_name = row['street_name']
#         storey_range = row['storey_range']
#         floor_area_sqm = row['floor_area_sqm']
#         flat_model = row['flat_model']
#         lease_commence_date = (row['lease_commence_date'])
#         remaining_lease = row['remaining_lease']
#         resale_price = row['resale_price']
#         image_path = row['image_path']

#         new_building = building(id = id, month = month, town = town, flat_type = flat_type, block = block, street_name = street_name, storey_range = storey_range, floor_area_sqm = floor_area_sqm, flat_model = flat_model, lease_commence_date = lease_commence_date, resale_price = resale_price, remaining_lease = remaining_lease, image_path = image_path)
#         db.session.add(new_building)
#         db.session.commit()
