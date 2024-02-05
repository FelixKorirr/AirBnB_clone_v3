#!/usr/bin/python3
"""Route for handling State objects and operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """Retrieves all State objects"""
    our_state_list = []
    our_state_obj = storage.all("State")
    for obj in our_state_obj.values():
        our_state_list.append(obj.to_json())

    return jsonify(our_state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """Create state route"""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new = State(**state_json)
    new.save()
    resp = jsonify(new.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """Gets a specific State object by ID"""

    my_obj = storage.get("State", str(state_id))

    if my_obj is None:
        abort(404)

    return jsonify(my_obj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """Updates specific State object by ID"""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    my_obj = storage.get("State", str(state_id))
    if my_obj is None:
        abort(404)
    for k, v in state_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(my_obj, k, v)
    my_obj.save()
    return jsonify(my_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """Deletes a state by id"""

    my_obj = storage.get("State", str(state_id))

    if my_obj is None:
        abort(404)

    storage.delete(my_obj)
    storage.save()

    return jsonify({})
