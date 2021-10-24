
from API import API_KEY
import googlemaps
from prettyprinter import pprint

client = googlemaps.Client(key=API_KEY)
geocode = client.geocode("ang mo kio")
pprint(geocode[0]['formatted_address'])
pprint(geocode[0]['geometry']['location']['lat'])
pprint(geocode[0]['geometry']['location']['lng'])

possibleReco = client.places_nearby(
    location=(str(geocode[0]['geometry']['location']['lat']) + "," + str(geocode[0]['geometry']['location']['lng'])), radius=2000, type="supermarket")

pprint(possibleReco)

for result in possibleReco['results']:
    pprint(result['name'])
    pprint(result['geometry']['location']['lat'])
    pprint(result['geometry']['location']['lng'])
