from .models import User, building
from . import db

def create_admin():


def import_buildings():
    from .models import building
    import os
    import pandas as pd
    from dateutil import parser

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

    # global list_of_buildings 
    # list_of_buildings = building.query.order_by(building.id).all()

create_admin()
# import_buildings()
# list_of_buildings = building.query.order_by(building.id).all()
# print(list_of_buildings[0])
print("a")