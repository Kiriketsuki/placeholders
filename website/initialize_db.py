import os
from re import M

import pandas as pd
from dateutil import parser
from werkzeug.security import generate_password_hash

from . import db
from .models import building
from .models import Preference
from .models import User
from .Recommender import Recommender

import random

def init_db():
    print("initializing db...")
    try:
        # create admin
        admin = User(
            firstName="admin",
            lastName="supreme",
            email="testing@gmail.com",
            password=generate_password_hash("password", method="sha256"),
        )
        db.session.add(admin)
        db.session.commit()

        # import buildings
        # todo change number in data.head() to whatever number of buildings you want to import
        file = "website/gov_data.csv"
        cwd = os.getcwd()
        data = pd.read_csv(os.path.normcase(os.path.join(cwd, file)))
        test = data[:500]

        # read from dataframe, create building, commit to db
        getLatLng = Recommender(None)

        for index, row in test.iterrows():
            month = parser.parse(row["month"])
            town = row["town"]
            flat_type = row["flat_type"]
            block = row["block"]
            street_name = row["street_name"]
            storey_range = row["storey_range"]
            floor_area_sqm = row["floor_area_sqm"]
            flat_model = row["flat_model"]
            lease_commence_date = row["lease_commence_date"]
            remaining_lease = row["remaining_lease"]
            resale_price = row["resale_price"]
            image_path = row['image_path']
            contact = row['contact']

#             latlng = getLatLng.getLatLng("block " + block + " " + street_name)

            new_building = building(
                lat=None,
                lng=None,
                month=month,
                town=town,
                flat_type=flat_type,
                block=block,
                street_name=street_name,
                storey_range=storey_range,
                floor_area_sqm=floor_area_sqm,
                flat_model=flat_model,
                lease_commence_date=lease_commence_date,
                resale_price=resale_price,
                remaining_lease=remaining_lease,
                image_path = image_path,
                contact = contact
            )
            db.session.add(new_building)
            db.session.commit()

        # # attach sample reccomendations to admin
        # for i in range(1,6):
        #     temp_building = building.query.filter_by(id = i).first()
        #     temp_building.recommended_to.append(admin)
        #     db.session.commit()

        # attach sample favourites to both guest and admin
#         for i in range(1,40):
#             temp_building = building.query.filter_by(id = i).first()
#             if (random.randint(0,1)):
#                 temp_building.favourited_by.append(admin)

        # create sample preferences for admin
        # temp_preference = Preference(
        #     houseType = "1 Room",
        #     budget = "below $300,000",
        #     monthlyIncome = "below $1,000",
        #     maritalStatus = "Single",
        #     cpf = "below $20,000",
        #     ownCar = False,
        #     amenities = ["Supermarket"],
        #     preferredLocations = ["Woodlands"],
        #     uid = 1 # guest's id
        # )
        # db.session.add(temp_preference)

        db.session.commit()
    except:
        return
