#!/usr/bin/python3
""" Objects that handle default Rest API actions for Place - Amenity """
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves a list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        all_amenities = [amenity.to_dict() for amenity in place.all_amenities]
    else:
        all_amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/all_amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object of a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.all_amenities:
            abort(404)
        place.all_amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/all_amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.all_amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.all_amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
