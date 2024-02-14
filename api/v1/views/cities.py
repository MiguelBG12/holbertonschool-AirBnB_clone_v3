#!/usr/bin/python3
"""City from states"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves a state object"""

    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    """Retrieves a city object"""

    list_cites = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_cities(city_id):
    """Delete a city object"""

    list_cites = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}, 200))


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def createCity(state_id):
    """Creates a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "name" not in data:
            return "Missing name", 400
        data["state_id"] = state_id
        objNew = City(**data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def updateCity(city_id):
    """Updates a State object"""
    city = storage.get(City, city_id)
    gitignore = ["id", "created_at", "updated_at", "state_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
    except Exception:
        if city is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400
