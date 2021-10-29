import json

import googlemaps
from flask_login import current_user
from googlemaps.maps import StaticMapMarker
from prettyprinter import pprint

from . import db
from .API import API_KEY
from .models import building
from .models import Recommendation
# API KEY FOR GOOGLE API


class Marker:
    def __init__(self, amenityList, fromLat, fromLng):
        self.client = googlemaps.Client(key=API_KEY)
        self.amenityList = amenityList
        self.fromLat = fromLat
        self.fromLng = fromLng

    def setMarkers(self):
        if self.amenityList != None:
            print(self.amenityList)
            amenityList = json.loads(self.amenityList)

            markerList = self.createMarkers(amenityList)
        else:
            markerList = self.createSingleMarker()

        result = self.client.static_map(size=[900, 900],
                                        zoom=17,
                                        scale=1,
                                        maptype="roadmap",
                                        markers=markerList)

        with open(f"website/static/Assets/map_img/marker.jpg", "wb+") as f:
            obj = list(result)
            for i in range(len(obj)):
                f.write(obj[i])
        # pprint(markerList)

    def createMarkers(self, amenityList):
        markerList = [
            StaticMapMarker(
                locations=[(i["geometry"]["location"]["lat"],
                            i["geometry"]["location"]["lng"])],
                color="red",
                size="large",
                label="A",
            ) for i in amenityList
        ]

        markerList.append(
            StaticMapMarker(
                locations=[(self.fromLat, self.fromLng)],
                color="purple",
                size="large",
                label="T",
            ))

        return markerList

    def createSingleMarker(self):
        return [
            StaticMapMarker(
                locations=[(self.fromLat, self.fromLng)],
                color="red",
                size="large",
                label="A",
            )
        ]
