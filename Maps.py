import requests


url = "https://maps.googleapis.com/maps/api/distancematrix/json"
key = "AIzaSyD5k5mIzmXQgdPK0d0CqxBmSQG3n4KjqmI"


def get_distance_in_seconds(frm: str, to: str):
    query = url + "?origins=" + frm + "&destinations=" + to + "&units=imperial&key=" + key
    response = requests.request("GET", query)
    data = response.json()
    distance = data["rows"][0]["elements"][0]["duration"]["value"]
    return distance
