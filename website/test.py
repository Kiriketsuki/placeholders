
# from werkzeug.local import F
# from API import API_KEY
# import googlemaps
# from googlemaps.maps import StaticMapMarker

# from prettyprinter import pprint

# client = googlemaps.Client(key=API_KEY)
# geocode = client.geocode("ang mo kio")
# pprint(geocode[0]['formatted_address'])
# pprint(geocode[0]['geometry']['location']['lat'])
# pprint(geocode[0]['geometry']['location']['lng'])
# print(type(geocode[0]['geometry']['location']['lng']))

# possibleReco = client.places_nearby(
#     location=(str(geocode[0]['geometry']['location']['lat']) + "," + str(geocode[0]['geometry']['location']['lng'])), radius=2000, type="supermarket")

# pprint(possibleReco["results"])

# # for count, item in enumerate(possibleReco["results"]):
# #     pprint(count+1)

# # print(len(possibleReco["results"]))
# # for result in possibleReco['results']:
# #     pprint(result['name'])
# #     pprint(result['geometry']['location']['lat'])
# #     pprint(result['geometry']['location']['lng'])

# # geocode2 = client.geocode("yishun")

# # matrix = client.distance_matrix((geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']), (
# #     geocode2[0]['geometry']['location']['lat'], geocode2[0]['geometry']['location']['lng']))

# # distance = matrix["rows"][0]["elements"][0]["distance"]["text"]
# # print(distance)
# # distance = ''.join((x for x in distance if x.isdigit() or x=='.'))
# # print(float(distance))

# marker = StaticMapMarker(
#     locations=[{"lat": -33.867486, "lng": 151.206990}, "Sydney"],
#     size="small",
#     color="blue",
#     label="S",
# )

# m1 = StaticMapMarker(
#     locations=[(geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng'])], color="blue", label="S"
# )

# m2 = StaticMapMarker(
#     locations=[(geocode2[0]['geometry']['location']['lat'], geocode2[0]['geometry']['location']['lng'])], size="large", color="green"
# )

# m3 = StaticMapMarker(
#     locations=["Tok,AK"], size="mid", color="0xFFFF00", label="C"
# )
                       
# res = client.static_map(size=[1000, 1000], zoom=13, scale=1, maptype='roadmap', markers=[m1, m2])

# with open("website/testimg.jpg", "wb") as f:
#     obj = list(res)
#     for i in range(len(obj)):
#         f.write(obj[i])

# print(list(res))

s = "Movie"
s = '_'.join(s.split(" "))
print(s)
