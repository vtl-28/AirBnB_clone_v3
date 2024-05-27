#!/usr/bin/python3
""" RESTFUL API for users """

from flask import request, abort, jsonify, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves all the users in the database """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves user in the database based on their ID """
    user = storage.get(User, user_id)
    if not user_id:
        abort(404)
    return jsonify(user.dict())


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def del_user(user_id):
    """
    Delete user in the database base on the passed ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new user and save it in the database """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(404, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates the user in the database on given ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'create_at', 'update_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
