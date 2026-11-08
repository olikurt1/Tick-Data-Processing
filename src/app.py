from flask import Flask, jsonify, abort, request
from datetime import date
from src.Store import get_sighting, count_by_region, search_sightings, count_by_period, count_sightings

#reads integer such as limit or offset, nothings passed then default offset used, checks if value is castable to int
def parse_int_parameter(name, default, min_value, max_value):
    value = request.args.get(name)
    if value is None:
        return default
    try:
        number = int(value)
    except ValueError:
        abort(400, description=f"'{name}' must be a whole number")
    #once parsed checks that value is within range
    if number < min_value or number > max_value:
        abort(400, description=f"'{name}' must be between {min_value} and {max_value}")
    return number    

#reads start and end dates, turns string date into actual date and raises error if date isn't iso standard
def parse_date_parameter(name):
    value = request.args.get(name)
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        abort(400, description=f"'{name}' must be a date like 2024-01-19")

#routes get attached to "app" and app lives in this module
app = Flask(__name__)

#Flask error handlers route custom functions for more specific error responses
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=e.description), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=e.description), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Internal server error"), 500


#endpoint for receiving filtered records
@app.get("/sightings")
def list_sightings():
    start_date = parse_date_parameter("start")
    end_date = parse_date_parameter("end")
    if start_date != None and end_date != None and start_date > end_date:
        abort(400, description="'start' must be before end")

    location = request.args.get("location")
    species = request.args.get("species")
    limit = parse_int_parameter("limit", 50, 1, 500)
    offset = parse_int_parameter("offset", 0, 0, 10_000)

    results = search_sightings(startDate=start_date, endDate=end_date, 
        locationFilter=location, 
        speciesFilter=species, 
        limit=limit, offset=offset
    )
    return jsonify(count=len(results), limit=limit, offset=offset, results=results)


#endpoint of grouped sightings by region
@app.get("/stats/by-region")
def sightings_by_region():
    return jsonify(count_by_region())


#endpoint to get single sighting by its ID
@app.get("/sightings/<sighting_id>")
def sighting_detail(sighting_id):
    sighting = get_sighting(sighting_id)
    if sighting is None:
        abort(404, description="Sighting not found")
    return jsonify (sighting)

#endpoint returning sightings by monthly or weekly periods
@app.get("/stats/by-period")
def sightings_by_period():
    period = request.args.get("period", "month")
    if period not in ("month", "week"):
        abort(400, description="'period' must be 'month' or 'week'")
    return jsonify(period=period, results=count_by_period(period))

#endpoint for checking health when parameter is added to url  
@app.get("/health")
def health():
    total = count_sightings()
    if total == 0:
        return jsonify(status="no data", sightings=0), 503
    return jsonify(status="ok", sightings=total)

