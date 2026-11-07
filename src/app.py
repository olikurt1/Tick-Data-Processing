from flask import Flask, jsonify
from src.Store import get_sightings, count_by_region

#routes get attached to "app" and app lives in this module
app = Flask(__name__)

#endpoint of grouped sightings by region
@app.get("/stats/by-region")
def sightings_by_region():
    return jsonify(count_by_region())

#endpoint to get single sighting by its ID
@app.get("/sightings/<sighting_id>")
def sighting_detail(sighting_id):
    sighting = get_sightings(sighting_id)
    if sighting is None:
        return jsonify(error="Sighting not found"), 404
    return jsonify (sighting)

