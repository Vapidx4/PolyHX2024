from googlemaps import convert
import googlemaps
import json
import math

def geocode(client, address, place_id=None, components=None, bounds=None, region=None,
            language=None):
    params = {}

    if address:
        params["address"] = address

    if place_id:
        params["place_id"] = place_id

    if components:
        params["components"] = convert.components(components)

    if bounds:
        params["bounds"] = convert.bounds(bounds)

    if region:
        params["region"] = region

    if language:
        params["language"] = language
    
    return client._request("/maps/api/geocode/json", params).get("results", [])

def findLocation(place):
    gmaps = googlemaps.Client(key='AIzaSyC7BjuLArIAW2SIg2ytPpXMPAlgmEULwC8')
    data = geocode(gmaps, place)
    firstItem = data[0]
    lat = math.radians(firstItem["geometry"]["location"]["lat"])
    lng = math.radians(firstItem["geometry"]["location"]["lng"])
    return [lat, lng]

def findDistance(location1, location2):
    list1 = findLocation(place = location1)
    list2 = findLocation(place = location2) 
    
    EARTH_RADIUS = 6371
    distance = 2 * EARTH_RADIUS * (math.sqrt(((1 - math.cos(list2[0] - list1[0])) / 2) + (math.cos(list1[0]) * math.cos(list2[0]) * (1 - math.cos(list2[1] - list1[1])) / 2)))
    return distance

print(findDistance("china", "old montreal"))
