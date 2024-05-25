#!/usr/bin/python3
""" City RESTFUL api actions """

from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/state/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    data['state_id'] = state_id
    city = City(**data)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/,city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in [id, state_id, create_at, update_at]:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
