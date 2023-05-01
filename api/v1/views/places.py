#!/usr/bin/python3
"""Place view"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a new Place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    data['city_id'] = city.id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object
    """
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """
    Searches for Place objects according to a JSON in the request body
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    if not data:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    if not isinstance(states, list) or not isinstance(cities, list)\
            or not isinstance(amenities, list):
        abort(400, "Invalid JSON format")
    places = []
    for place in storage.all(Place).values():
        if (not states or place.city.state_id in states) and\
                (not cities or place.city_id in cities):
            if all(amenity.id in [a.id for a in place.amenities]
                    for amenity in amenities):
                places.append(place)
    return jsonify([place.to_dict() for place in places])
