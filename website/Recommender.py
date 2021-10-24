import googlemaps
import time

from sqlalchemy.sql.expression import true
from .models import building
from .models import recommendations
from .models import Recommendation
from .models import building
from .models import Preference
from .models import User
from flask_login import current_user
from . import db

# API KEY FOR GOOGLE API
from .API import API_KEY
from prettyprinter import pprint

# Returns the list of building ids to recommend
class Recommender():
    def __init__(self, preference):
        self.client = googlemaps.Client(key=API_KEY)
        self.preference = preference

    def getLngLat(self, location):
        # Convert location to longitude latitude
        geocode = self.client.geocode(location) # geocode is a json response

        # return address, longitude, latitude
        return dict(address=geocode[0]['formatted_address'], lat=geocode[0]['geometry']['location']['lat'], lng=geocode[0]['geometry']['location']['lng'])

    # return unrecommended list of locations based on user preferred loc
    def getBuildingsByPref(self):
        preferredLoc = self.preference.preferredLocations # get user's preferred loc
        '''
        Match all possible loc in db with user's preferred loc.
        loc is an array of building references
        '''
        loc = building.query.filter_by(town = preferredLoc[0].upper()).all() 

        switch = {"below $300,000": 300000, "$300,000 to $400,000": 400000, "$500,000 to $600,000": 600000, "$600,000 to $700,000": 700000, "$700,000 to $800,000": 800000, "$800,000 to $1,000,000": 1000000, "above $1,000,000": -1000000}

        # filter loc array according to user's house type and budget
        idx = 0
        while (idx < len(loc)):
            if loc[idx].flat_type != self.preference.houseType.upper() or loc[idx].resale_price > switch[self.preference.budget]:
                loc.pop(idx)
            else:
                idx+=1
            
        return loc  # returns array of buildings

    def findRecommendations(self):
        loc = self.getBuildingsByPref()

        # {Building : value} pairs
        # Each {Building: value} pair contains a dict of
        # {address: , latitude: , longitude: }
        loc_dict = {loc[i]: self.getLngLat("block" + loc[i].block + " " + loc[i].street_name) for i in range(len(loc))}

        # store each building and their amenities nearby
        building_reco_dict = {}
        for idx, blk in enumerate(loc_dict):
            bldng = loc[idx]
            reco = self.client.places_nearby(
                location=(str(loc_dict[blk]["lat"]) + "," + str(loc_dict[blk]["lng"])), radius=1000, type=self.preference.amenities[0])
            if reco:
                building_reco_dict[bldng] = reco["results"]
                addRecommended = building.query.filter_by(id=bldng.id).first()
                addRecommended.recommended_to.append(current_user)

        # pprint(building_reco_dict)

        # newRecommendation = Recommendation(user_id=current_user.get_id(), building_ids=building_reco_dict)
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
        self.findRecommendations()
