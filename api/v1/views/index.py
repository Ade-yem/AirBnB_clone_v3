#!/usr/bin/python3
"""Index view"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """status of the web app"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of each objects by type"""
    # Define a list of object types to count
    obj_types = ["Amenity", "City", "Place", "Review", "State", "User"]
    
    # Use a dictionary comprehension to count objects of each type and store in a dictionary
    counts = {t.lower() + 's': storage.count(t) for t in obj_types}
    
    # Return the counts as a JSON response
    return jsonify(counts)
