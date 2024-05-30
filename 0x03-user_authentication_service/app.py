#!/usr/bin/env python3
""" app Flask """
from flask import Flask, jsonify, request, make_response
from flask import abort, Response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Response:
    """login"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        jsoni = jsonify({"email": email, "message": "logged in"}), 200
        response = make_response(jsoni)
        response.set_cookie("session_id", AUTH.create_session(email))
        return response

    abort(401)


@app.route("/users", methods=["POST"])
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/", methods=["GET"])
def welcome() -> Response:
    """doc doc doc"""
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """doc doc doc"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
