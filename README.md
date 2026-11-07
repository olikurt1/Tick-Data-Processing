# Tick-Data-Processing

## Overview

This program is a Flask API backend which provides endpoints for querying tick sightings pulled from the Elanco public API. The data is fetched using requests, cleaned using pandas and stored in an sqlite3 database. The program includes testing for Clean and Fetch to showcase in the event that an error does need handling, the error handlers do work. 

## How to run

To run the program:
- Clone the repository
- Create a virtual environment and run pip install -r requirements.txt, this will install all the dependencies required for running the program
- run python -m src.sync from the root of the folder, this will run the core programs
- run flask --app src.app run. This will run the API server that receieves requests for endpoints in app.py s

## Endpoints

| Method | Path | Parameters | Example |
|--------|------|------------|---------|
| GET | '/sightings' | 'start', 'end', 'location', 'species', 'limit', 'offset' | '/sightings?location=leeds&limit=20 |
| GET | 'sightings/<sighting_id> | None | 'sightings/idxxxxxxx |
| GET | '/stats/by-region' | None | '/stats/by-region' |
| GET | 'stats/by-period' | 'period' ('month' or 'week') | '/stats/by-period?period=week' |
| GET | '/health' | None | '/health' | 

