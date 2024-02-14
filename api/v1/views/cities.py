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