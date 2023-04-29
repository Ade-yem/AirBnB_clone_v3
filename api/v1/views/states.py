#!/usr/bin/python3
"""States view"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from flask import request, abort


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def show_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def show_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for k, v in request.get_json().items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200


