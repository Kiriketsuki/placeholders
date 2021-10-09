from . import db
from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# association table
recommendations = db.Table('recommendations',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('building_id', db.Integer, db.ForeignKey('building.id'))
)
# User schema
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    recommended = db.relationship('building', secondary = recommendations, backref = db.backref('recommended_to', lazy = 'dynamic'))
    pid = db.relationship('Preference', backref='user', uselist=False)

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseType = db.Column(db.String(150))
    budget = db.Column(db.String(150))
    maritalStatus = db.Column(db.String(150))
    cpf = db.Column(db.String(150))
    ownCar = db.Column(db.Boolean)
    amenities = db.Column(db.JSON)
    preferredLocations = db.Column(db.JSON)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=True)

# building schema
class building(db.Model):
    id = db.Column(db.Integer, primary_key = True)
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

