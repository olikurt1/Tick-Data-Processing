from flask import Flask, jsonify, abort
from src.Store import get_sighting, count_by_region

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

