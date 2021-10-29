import googlemaps

from .models import building
from .models import Recommendation
from .models import building
from flask_login import current_user
from . import db
import json

# API KEY FOR GOOGLE API
from .API import API_KEY
from prettyprinter import pprint

# Returns the list of building ids to recommend
class Recommender():
    def __init__(self, preference):
        # init client
        self.client = googlemaps.Client(key=API_KEY)

        # users current list of prefences in db
        self.preference = preference

    def getLatLng(self, location):
        # Convert location to longitude latitude
        geocode = self.client.geocode(location)  # geocode is a json response

        # return dict {address, latitude, longitude}
        return geocode[0]['formatted_address'], geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']

    def distanceMatrix(self, latFrom, lngFrom, toLat, toLng):
        matrix = self.client.distance_matrix(
            (latFrom, lngFrom), (toLat, toLng))

        return matrix["rows"][0]["elements"][0]["distance"]["text"]

    # return list of locations based on user preferred loc
    def getBuildingsByPref(self):
        # get user's preferred loc
        preferredLoc = self.preference.preferredLocations

        # Match all possible loc in db with user's preferred loc.
        # loc is an array of building references
        loc = building.query.filter_by(town=preferredLoc[0].upper()).all()

        switch = {"below $300,000": 300000, "$300,000 to $400,000": 400000, "$400,000 to $500,000": 500000, "$500,000 to $600,000": 600000,
                  "$600,000 to $700,000": 700000, "$700,000 to $800,000": 800000, "$800,000 to $1,000,000": 1000000, "above $1,000,000": float("inf")}

        # filter loc array according to user's house type and budget
        idx = 0
        while (idx < len(loc)):
            if loc[idx].flat_type != self.preference.houseType.upper() or loc[idx].resale_price > switch[self.preference.budget]:
                loc.pop(idx)
            else:
                idx += 1

        return loc # returns filtered array of buildings based on location & budget

    def filterByDistance(self, latFrom, lngFrom, amenityList):
        item = 0
        while (item < len(amenityList)):
            distance = self.distanceMatrix(
                latFrom, lngFrom, amenityList[item]["geometry"]["location"]["lat"], amenityList[item]["geometry"]["location"]["lng"])
            distance = ''.join((x for x in distance if x.isdigit() or x == '.'))

            # if amenity < threshold distance in km
            if float(distance) < self.preference.distance:
                # print(float(distance))
                amenityList.pop(item)
            
            item+=1

        return amenityList

    def findRecommendations(self):
        loc = self.getBuildingsByPref()

        amenityPreference = self.preference.amenities[0].lower()
        amenityPreference = "_".join(amenityPreference.split(" "))
        print(amenityPreference)

        for item in loc:
            query = db.session.execute(f"SELECT * FROM building WHERE id={item.id}").first()

            if query.lat and query.lng != None:
                latitude = query.lat
                longitude = query.lng
            else:
                addr, latitude, longitude = self.getLatLng("block " + query.block + " " + query.street_name)
                db.session.execute(f"UPDATE building SET lat={latitude}, lng={longitude} WHERE id={item.id}")
                # query.lat = latitude
                # query.lng = longitude
                # db.commit()

            print(latitude, longitude)
            # find nearby amenities

            hasAmenities = self.client.places_nearby(
                        location=(str(latitude) + "," + str(longitude)), radius=500, type=amenityPreference)
            
            # list of recommendations filtered by distance < x km from target location {where x is the user defined distance preference}
            result = self.filterByDistance(latitude, longitude, hasAmenities["results"])

            print("finding recommendations...")
            # pprint(result)
            
            # add to reommendation table in db
            if result != []:
                newRecommendation = Recommendation(user_id=current_user.get_id(), building_id=item.id, amenities_type=self.preference.amenities[0], amenities_list=result, num_amenities=len(result))

                db.session.add(newRecommendation)
                db.session.commit()

    def run(self):
        # delete old recommendations to update with new ones
        if Recommendation.query.filter_by(user_id=current_user.get_id()).first():
            Recommendation.query.filter_by(
                user_id=current_user.get_id()).delete()
            db.session.commit()

        self.findRecommendations()
