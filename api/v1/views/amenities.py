#!/usr/bin/python3
"""Objects that handle all default REStfull api actions for amenities"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrives the list of ameneties"""
    all_amenities = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrives amenty of objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create an amenity"""
    amenity = request.get_json()
    if request.is_json:
        if "name" not in amenity:
            return "Missing name", 400
        objNew = Amenity(**amenity)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity object"""
    amenities = storage.get(Amenity, amenity_id)
    gitignore = ["id", "created_at", "updated_at", "state_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(amenities, k, v)
        storage.save()
        return jsonify(amenities.to_dict()), 200
    except Exception:
        if amenities is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400
