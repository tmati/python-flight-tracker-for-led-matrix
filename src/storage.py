import json
import os
from datetime import datetime

#Write and read flight info from .txt file cache

DATA_FILE = "data/flightcache.txt"

def save_flight_info(flight_info):
    flight_info["timestamp"] = datetime.now().isoformat()
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(flight_info, f)
    except Exception as e:
        print(f"Error saving flight info: {e}")


def load_flight_info():
    """
    Load flight info from file.
    Returns a dictionary or None if no valid data found.
    """
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as f:
            flight_info = json.load(f)
            return flight_info
    except Exception as e:
        print(f"Error loading flight info: {e}")
        return None