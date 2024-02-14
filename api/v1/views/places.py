#!/usr/bin/python3
"""Objects that handle all default REStfull api actions for places"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_city_places(city_id):
    """Retrieves all places of a city"""
    all_places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Creates a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "user_id" not in data:
            return "Missing user_id", 400
        if "name" not in data:
            return "Misiing name", 400
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        objNew = Place(city_id=city_id, **data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates an existing place"""
    place = storage.get(Place, place_id)
    gitignore = ["id", "city_id", "created_at", "updated_at", "user_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
    except Exception:
        if place is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400
