import googlemaps

from .models import building
from .models import Recommendation
from .models import building
from flask_login import current_user
from . import db

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

    def getLngLat(self, location):
        # Convert location to longitude latitude
        geocode = self.client.geocode(location)  # geocode is a json response

        # return dict {address, latitude, longitude}
        return dict(address=geocode[0]['formatted_address'], lat=geocode[0]['geometry']['location']['lat'], lng=geocode[0]['geometry']['location']['lng'])

    def distanceMatrix(self, latFrom, lngFrom, latTo, lngTo):
        matrix = self.client.distance_matrix(latFrom, lngFrom. latTo, lngTo)
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

        return loc  # returns filtered array of buildings based on location & budget

    def findRecommendations(self):
        loc = self.getBuildingsByPref()

        # {Building : value} pairs
        # Each {Building: value} pair contains a dict of
        # {address: , latitude: , longitude: }
        loc_dict = {loc[i]: self.getLngLat(
            "block" + loc[i].block + " " + loc[i].street_name) for i in range(len(loc))}

        # store each building and their nearby amenities
        for idx, blk in enumerate(loc_dict):
            bldng = loc[idx]
            reco = self.client.places_nearby(
                location=(str(loc_dict[blk]["lat"]) + "," + str(loc_dict[blk]["lng"])), radius=500, type=self.preference.amenities[0])
            if reco:
                addRecommended = building.query.filter_by(id=bldng.id).first()
                addRecommended.recommended_to.append(current_user)

                newRecommendation = Recommendation(user_id=current_user.get_id(
                ), building_id=bldng.id, amenities_type=self.preference.amenities[0], amenities_list=reco["results"], num_amenities=len(reco["results"]))

                db.session.add(newRecommendation)
                db.session.commit()

        # pprint(building_reco_dict)

        # newRecommendation = Recommendation(user_id=current_user.get_id(),   building_ids=building_reco_dict)
        # db.session.add(newRecommendation)
        # db.session.commit()

        # print(thisRecommendation)
        # reco_dict = dict(name=None, lat=None, lng=None)
        # for result in reco['results']:
        #     reco_dict["name"] = result["name"]
        #     reco_dict["lat"] = result["geometry"]["location"]["lat"]
        #     reco_dict["lng"] = result["geometry"]["location"]["lng"]
        #     newRecommendation = recommendations(user_id=current_user.get_id(), building_id=)
        # pprint(reco_dict)

    def run(self):
        if Recommendation.query.filter_by(user_id=current_user.get_id()).first():
            Recommendation.query.filter_by(
                user_id=current_user.get_id()).delete()
            db.session.commit()

        self.findRecommendations()
