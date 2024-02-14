#!/usr/bin/python3
"""Objects to handle all default REStfull APi actions for states"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all state objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a state object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}, 200))


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def createStates():
    """Creates a State"""
    if request.is_json:
        data = request.get_json()
        if "name" not in data:
            return "Missing name", 400
        objNew = State(**data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def updateState(state_id):
    """Updates a State object"""
    states = storage.get(State, state_id)
    gitignore = ["id", "created_at", "updated_at"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(states, k, v)
        storage.save()
        return jsonify(states.to_dict()), 200
    except Exception:
        if states is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400
