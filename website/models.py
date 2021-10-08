from . import db
from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

