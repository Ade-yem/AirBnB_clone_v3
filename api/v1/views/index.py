#!/usr/bin/python3
"""Index view"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """status of the web app"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """stats of the database"""
    cnt_dict = {}
    cls_list = ["State", "City", "Amenity", "User", "Place", "Review"]
    for clas in cls_list:
        num = storage.count(clas)
        cnt_dict[clas] = num
    return jsonify(cnt_dict)

