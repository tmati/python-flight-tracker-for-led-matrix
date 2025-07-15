import time
import requests
import json
import os
    
CONFIG_PATH = "data/special_callsigns.json"

def fetch_nearby_flight_from_opensky():
    #TODO This could be set like so that it determines the closest flight to user-submitted coordinates from available flights and returns information of that to the user.

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
        for state in states:
            # TODO maybe add state[11] here for vertical rate - filter by descending when vert rate is negative
            # TODO also state [17] category information could also be interesting, but it seems to be empty most of the time on OpenSky...
            callsign = state[1].strip()
            if callsign:
                return callsign
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
    callsign = fetch_nearby_flight_from_opensky()

    if callsign:
        flight_details = fetch_adsb_info(callsign)
        return {
            "callsign": callsign,
            "airlineName": flight_details.get("airline", {}).get("name", "Unknown airline"),
            "airlineOrigin": flight_details.get("airline", {}).get("country", "Unknown airline country"),
            "airlineCountryIso": flight_details.get("airline", {}).get("country_iso", "Unknown airline country ISO"),
            "departure": flight_details.get("origin", {}).get("iata_code", "Unknown departure IATA"),
            "departureIcao": flight_details.get("origin", {}).get("icao_code", "Unknown departure ICAO"),
            "departureMunicipality": flight_details.get("origin", {}).get("municipality", "Unknown departure municipality"),
            "departureAirportName": flight_details.get("origin", {}).get("name", "Unknown departure municipality name")
        }


def load_special_callsigns():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading callsign config: {e}")
    return {}