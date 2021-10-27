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

    def distanceMatrix(self, latFrom, lngFrom, latTo, lngTo):
        matrix = self.client.distance_matrix(latFrom, lngFrom. latTo, lngTo)
        return matrix["rows"][0]["elements"][0]["distance"]["text"]

    def getLngLat(self, location):
        # Convert location to longitude latitude
        geocode = self.client.geocode(location)  # geocode is a json response

        # return dict {address, latitude, longitude}
        return dict(address=geocode[0]['formatted_address'], lat=geocode[0]['geometry']['location']['lat'], lng=geocode[0]['geometry']['location']['lng'])

    # filter amenities if their distance from target location < 2km
    def filterAmenities(self):
        amenities = db.session.execute(f"select user_id, building_id, amenities_list from recommendation where user_id={current_user.get_id()}").all()

        return amenities

    def filterByDistance(self, amenities):
        for amenity in amenities:
            amenityList = json.loads(amenity.amenities_list)
            for item in amenityList:
                distance = self.distanceMatrix(item)
                distance = ''.join((x for x in distance if x.isdigit() or x == '.'))
                print(item["geometry"]["location"]["lat"],
                       item["geometry"]["location"]["lng"])
            # i = 0
            # amenityList = json.loads(amenity.amenities_list[i+1])
            # while (i < len(amenityList)):
            #     print(amenityList[i+1])
            #     i+=1
        
        # x_json = json.loads(amenities[0].amenities_list)
        # pprint(x_json[1])

    def run(self):
        amenities = self.filterAmenities()
        self.filterByDistance(amenities)
