#!/usr/bin/env python3
""" View for Session Authentication
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


auth = SessionAuth()


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles user login with session authentication """
    email = request.form.get('email')
    password = request.form.get('password')

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)
    return response
