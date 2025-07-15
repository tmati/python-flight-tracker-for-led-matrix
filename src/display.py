from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Setup matrix options
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Adjust based on panel type

matrix = RGBMatrix(options=options)

# Load font
font = graphics.Font()
font.LoadFont("fonts/6x10.bdf")  # Make sure this file exists

def send_to_led(flight_info):
    """
    Displays flight info (callsign + airline, departure) on the LED matrix.
    """
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()

    # Two lines
    # Callsign, airline, airline home country
    # Departure airport IATA, departure city, departure airport name

    # Extract and format text
    line1 = f"{flight_info.get('callsign', 'Unknown callsign')} {flight_info.get('airlineName', 'Unknown airline')} {flight_info.get('airlineCountryIso', 'XX')}"
    line2 = f"DEPARTURE: {flight_info.get('departure', 'unknown IATA')} {flight_info.get('departureMunicipality', 'Unknown city')} {flight_info.get('departureAirportName', 'Unknown airport')}"

    # Draw both lines
    graphics.DrawText(canvas, font, 2, 12, graphics.Color(255, 255, 0), line1)
    graphics.DrawText(canvas, font, 2, 24, graphics.Color(0, 255, 255), line2)

    canvas = matrix.SwapOnVSync(canvas)