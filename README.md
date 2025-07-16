# Flight tracker project for LED Matrix


The goal of this project is to show nearby flights using OpenSky Network API to collect ADS-B callsigns from a geographical bounding box area. One of the found callsigns will then be queried from ADSBDB API to find information about the carrier and the place of departure.

The long term goal is to install the script to a Raspberry PI ZERO, and configure it to transmit the data to a LED matrix display for viewing. The script will then run every now and then to provide updated information of nearby flight activities.


# Features

- [x]  Query flight data from a geographic area from OpenSky Network API
- [x] Use callsign queried from OpenSky to call ADSBDB API for further flight information
- [x] Write found information of latest flight into text file for caching
- [x] Read information from cache if no update for flight information is available
- [x] draft code for displaying data on LED matrix using [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) (Needs Raspberry Pi host and LED matrix in GPIO to work)
- [x] Error handling and secure defaults for flights where ADSBDB doesn't return anything
- [x] Special callsigns list to get information for e.g. HEMS services that usually do not serve it, even if their callsign is found.
- [x] Mapper for aircraft type information
- [x] Use preset location information to show information of closest flight based on specified coordinates and coordinates of flight. Manage user coordinates as secrets.


# TODO

- [ ] Bounding box coordinate information as function parameters to OpenSky URL
- [ ] Show latest airport arrival info via OpenSky and airport ICAO. Manage ICAO as secret.
- [ ] Logging? e.g. track daily request amount to keep track of rate limits
- [ ] Set up scheduled scanning (probably cron task on RPi)
- [ ] Set up credentials and OAuth2.0 for OpenSky API to increase rate limits if necessary. Handle credentials as secrets
- [ ] Design custom layout for flight data on LED matrix