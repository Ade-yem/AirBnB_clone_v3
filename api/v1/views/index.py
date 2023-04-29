#!/usr/bin/python3
"""Index view"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """status of the web app"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Retrieves the number of each objects by type"""
    # Get counts of each object type using count() method from storage
    amenity_count = storage.count("Amenity")
    city_count = storage.count("City")
    place_count = storage.count("Place")
    review_count = storage.count("Review")
    state_count = storage.count("State")
    user_count = storage.count("User")
    
    # Return JSON response with counts for each object type
    return jsonify({
        "amenities": amenity_count,
        "cities": city_count,
        "places": place_count,
        "reviews": review_count,
        "states": state_count,
        "users": user_count
    })

