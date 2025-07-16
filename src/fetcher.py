import requests
import json
from src import planefinder
    
CONFIG_PATH = "data/special_callsigns.json"

def fetch_nearby_flight_from_opensky():

    # Query OpenSky for flights in a coordinate square between Strömsö and Helsinki-Vantaa
    opensky_api_url = "https://opensky-network.org/api/states/all?lamin=59.8887&lomin=23.7885&lamax=60.3228&lomax=24.8743&extended=1"
    # debug url for Helsinki-Vantaa airport :)
    opensky_api_url_efhk = "https://opensky-network.org/api/states/all?lamin=60.292994&lomin=24.857327&lamax=60.339456&lomax=24.997544&extended=1"
    # Switzerland
    opensky_api_url_sui = "https://opensky-network.org/api/states/all?lamin=45.8389&lomin=5.9962&lamax=47.8229&lomax=10.5226&extended=1"

    try:
        response = requests.get(opensky_api_url)
        response.raise_for_status()
        data = response.json()
        states = data.get("states", [])
        
        closestAircraft = planefinder.find_closest_aircraft(states)

        # TODO maybe add state[11] here for vertical rate - filter by descending when vert rate is negative
        callsign = closestAircraft[1].strip()
        category = closestAircraft[17] if len(closestAircraft) > 17 else None
        if callsign:
            return {
                "callsign": callsign,
                "category": category
            } 
    except Exception as e:
        if "NoneType" in str(e):
            # no aircraft in scan area — don't print error!
            return None
        else:
            print(f"Unexpected OpenSky error: {e}")
            return None


# Fetch additional info from ADSBDB with callsign found from OpenSky
def fetch_adsb_info(callsign):

    special_callsigns = load_special_callsigns()

    if callsign in special_callsigns:
        print("Using local config for special callsign.")
        return special_callsigns[callsign]

    print(f"Calling ADSBDB with callsign " + callsign)
    try: 
        adsbdb_url = f"https://api.adsbdb.com/v0/callsign/{callsign}"
        response = requests.get(adsbdb_url)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("flightroute", {})
    except requests.exceptions.HTTPError as e:
        print(f"ADSBDB HTTP error: {e}")
        check_adsbdb_online()
    except Exception as e:
        print(f"ADSBDB error: {e}")
    return {}


def check_adsbdb_online():
    
    adsbdb_healthcheck_endpoint="https://api.adsbdb.com/v0/online"
    try:
        response = requests.get(adsbdb_healthcheck_endpoint)
        response.raise_for_status()
        status = response.json()
        print(f"ADSBDB status: {status}")
    except Exception as e:
        print(f"ADSBDB health check failed: {e}")


def get_flightdata():
    # Complete flight data flow - Opensky for callsign, ADSBDB for further info.
    openskyInfo = fetch_nearby_flight_from_opensky()

    if openskyInfo:
        callsign = openskyInfo.get("callsign")
        category_code = openskyInfo.get("category")
        flight_details = fetch_adsb_info(callsign)
        return {
            "callsign": callsign,
            "airlineName": flight_details.get("airline", {}).get("name", "Unknown airline"),
            "airlineOrigin": flight_details.get("airline", {}).get("country", "Unknown airline country"),
            "airlineCountryIso": flight_details.get("airline", {}).get("country_iso", "Unknown airline country ISO"),
            "departure": flight_details.get("origin", {}).get("iata_code", "Unknown departure IATA"),
            "departureIcao": flight_details.get("origin", {}).get("icao_code", "Unknown departure ICAO"),
            "departureMunicipality": flight_details.get("origin", {}).get("municipality", "Unknown departure municipality"),
            "departureAirportName": flight_details.get("origin", {}).get("name", "Unknown departure municipality name"),
            "aircraftCategory": AIRCRAFT_CATEGORIES.get(category_code, AIRCRAFT_CATEGORIES[0])
        }


def load_special_callsigns():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading callsign config: {e}")
    return {}


AIRCRAFT_CATEGORIES = {
    0: "No information",
    1: "No ADS-B Emitter information",
    2: "Light",
    3: "Small",
    4: "Large",
    5: "High Vortex Large",
    6: "Heavy",
    7: "High Performance",
    8: "Rotorcraft",
    9: "Glider / sailplane",
    10: "Lighter-than-air",
    11: "Parachutist / Skydiver",
    12: "Ultralight / hang-glider / paraglider",
    13: "Reserved",
    14: "Unmanned Aerial Vehicle",
    15: "Space / Trans-atmospheric vehicle",
    16: "Surface Vehicle - Emergency Vehicle",
    17: "Surface Vehicle - Service Vehicle",
    18: "Point Obstacle",
    19: "Cluster Obstacle",
    20: "Line Obstacle"
}