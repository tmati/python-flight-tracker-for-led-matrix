from math import radians, sin, cos, sqrt, atan2
from dotenv import load_dotenv
import os

# Add your latitude and longitude details to .env file with OBSERVER_LAT and OBSERVER_LON to measure distance of aircraft to your given position
load_dotenv()
observer_lat = float(os.getenv("OBSERVER_LAT"))
observer_lon = float(os.getenv("OBSERVER_LON"))


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km


def find_closest_aircraft(states):

    closest = None
    min_distance = float("inf")

    for state in states:
        aircraft_lat = state[6]
        aircraft_lon = state[5]

        if aircraft_lat is not None and aircraft_lon is not None and state[1] is not None:
            dist = haversine(observer_lat, observer_lon, aircraft_lat, aircraft_lon)
            print(f"Found callsign {state[1].strip()} at distance of {round(dist)} km")
            if dist < min_distance :
                min_distance = dist
                closest = state

    return closest