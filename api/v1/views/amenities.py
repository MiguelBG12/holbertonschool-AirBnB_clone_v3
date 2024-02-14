#!/usr/bin/python3
"""objects that handle all default REStfull api actions for amenities"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrives the list of ameneties"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)
