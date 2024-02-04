from googlemaps import convert
import googlemaps
import json
import math

def geocode(client, address, place_id=None, components=None, bounds=None, region=None,
            language=None):
    """
    Geocoding is the process of converting addresses
    (like ``"1600 Amphitheatre Parkway, Mountain View, CA"``) into geographic
    coordinates (like latitude 37.423021 and longitude -122.083739), which you
    can use to place markers or position the map.

    :param address: The address to geocode.
    :type address: string

    :param place_id: A textual identifier that uniquely identifies a place,
        returned from a Places search.
    :type place_id: string

    :param components: A component filter for which you wish to obtain a
        geocode, for example: ``{'administrative_area': 'TX','country': 'US'}``
    :type components: dict

    :param bounds: The bounding box of the viewport within which to bias geocode
        results more prominently.
    :type bounds: string or dict with northeast and southwest keys.

    :param region: The region code, specified as a ccTLD ("top-level domain")
        two-character value.
    :type region: string

    :param language: The language in which to return results.
    :type language: string

    :rtype: list of geocoding results.
    """

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

# list1 = findLocation(place = "montreal")
# list2 = findLocation(place = "mexico")

list1 = [math.radians(45.4532), math.radians(-73.5818)]
list2 = [math.radians(45.5353), math.radians(-73.7231)]

print(list1)

EARTH_RADIUS = 6371

distance = 2 * EARTH_RADIUS * (math.sqrt(((1 - math.cos(list2[0] - list1[0])) / 2) + (math.cos(list1[0]) * math.cos(list2[0]) * (1 - math.cos(list2[1] - list1[1])) / 2)))
