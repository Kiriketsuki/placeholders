import googlemaps

from .models import building
from .models import Recommendation
from .models import building
from flask_login import current_user
from . import db

# API KEY FOR GOOGLE API
from .API import API_KEY
from prettyprinter import pprint

import json

class Mapper():
    def __init__(self):
        self.client = googlemaps.Client(key=API_KEY)


    def getLatLng(self, location):
        # Convert location to longitude latitude
        geocode = self.client.geocode(location)  # geocode is a json response

        # return dict {address, latitude, longitude}
        return dict(address=geocode[0]['formatted_address'], lat=geocode[0]['geometry']['location']['lat'], lng=geocode[0]['geometry']['location']['lng'])

    def distanceMatrix(self, latFrom, lngFrom, toLat, toLng):
        matrix = self.client.distance_matrix((latFrom, lngFrom), (toLat, toLng))

        return matrix["rows"][0]["elements"][0]["distance"]["text"]

    # filter amenities if their distance from target location < 2km
    def filterAmenities(self):
        query = db.session.execute(
            f"select user_id, building_id, block, street_name, amenities_list from recommendation r, building b where user_id={current_user.get_id()} and r.building_id = b.id").all()

        return query

    def filterByDistance(self, table):
        for attr in table:
            # get current building's lat lng
            currentBuildingAddress = "block " + attr.block + attr.street_name
            fromLatLng = self.getLatLng(currentBuildingAddress)

            # convert amenities_list into json
            amenityList = json.loads(attr.amenities_list)

            item = 0
            while (item < len(amenityList)):
                distance = self.distanceMatrix(
                    fromLatLng["lat"], fromLatLng["lng"], amenityList[item]["geometry"]["location"]["lat"], amenityList[item]["geometry"]["location"]["lng"])
                distance = ''.join((x for x in distance if x.isdigit() or x == '.'))

                if float(distance) < 2:
                    amenityList.pop(item)

                item+=1

            Recommendation.query.filter_by(building_id=attr.building_id).update(dict(amenities_list=amenityList, num_amenities=len(amenityList)))

            db.session.commit()
                
    def run(self):
        result = self.filterAmenities()
        self.filterByDistance(result)
