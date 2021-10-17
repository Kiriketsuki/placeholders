import os

import pandas as pd
from dateutil import parser
from werkzeug.security import generate_password_hash

from . import db
from .models import building
from .models import Preference
from .models import User

def init_db():
    try:
        print("entered")
        # create admin
        admin = User(
            firstName="admin",
            lastName="supreme",
            email="testing@gmail.com",
            password=generate_password_hash("password", method="sha256"),
        )
        db.session.add(admin)
        db.session.commit()

        # create guest
        guest = User(
            firstName="guest",
            lastName="",
            email="guest@gmail.com",
            password=generate_password_hash("", method="sha256")
        )
        db.session.add(guest)
        db.session.commit()

        # import buildings
        # todo change 5 to whatever number of buildings you want to import
        file = "website/gov_data.csv"
        cwd = os.getcwd()
        data = pd.read_csv(os.path.normcase(os.path.join(cwd, file)))
        test = data.head(10)  # adding only 5

        # read from dataframe, create building, commit to db
        for index, row in test.iterrows():
            id = row["_id"]
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
            new_building = building(
                id=id,
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
                image_path = image_path
            )
            db.session.add(new_building)
            db.session.commit()

        # attach sample reccomendations to admin
        for i in range(1,6):
            temp_building = building.query.filter_by(id = i).first()
            temp_building.recommended_to.append(admin)
            db.session.commit()

        for i in range(6,11):
            temp_building = building.query.filter_by(id = i).first()
            temp_building.recommended_to.append(guest)
            db.session.commit()

        # attach sample favourites to both guest and admin
        for i in range(1,6):
            temp_building = building.query.filter_by(id = i).first()
            temp_building.favourited_by.append(admin)
            temp_building.favourited_by(guest)
            db.session.commit()

        db.session.commit()
    except:
        return