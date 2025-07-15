from datetime import datetime
from src import fetcher, storage
#import display as well when on unix

flightInfo = fetcher.get_flightdata()
if flightInfo:
    storage.save_flight_info(flightInfo)
else:
    print("No new flight found — using cached data.")
    flightInfo = storage.load_flight_info()

if flightInfo:
    timestamp = flightInfo.get("timestamp")
    if timestamp:
        saved_time = datetime.fromisoformat(timestamp)
        age_minutes = (datetime.now() - saved_time).total_seconds() // 60
        print(f"Cached flight info from {saved_time.strftime('%Y-%m-%d %H:%M:%S')} ({int(age_minutes)} min ago)")
    else:
        print("Cached flight info has no timestamp.")
    # If you have a LED panel, try this:
    # display.send_to_led(flightInfo)
    
    # We just print for now...
    print(f"Callsign: {flightInfo.get('callsign', 'Unknown callsign')}")
    print(f"Airline: {flightInfo.get('airlineName', 'Unknown airline')}")
    print(f"Airline origin country: {flightInfo.get('airlineOrigin', 'Unknown airline origin')}")
    print(f"Airline origin ISO code: {flightInfo.get('airlineCountryIso', 'Unknown airline country ISO')}")

    print(f"Departure: {flightInfo.get('departure', 'Unknown departure IATA')}")
    print(f"Departure ICAO: {flightInfo.get('departureIcao', 'Unknown departure ICAO')}")
    print(f"Departure municipality: {flightInfo.get('departureMunicipality', 'Unknown departure municipality')}")
    print(f"Departure airport name: {flightInfo.get('departureAirportName', 'Unknown departure airport')}")