#!/usr/bin/env python3
""" app Flask """
from flask import Flask, jsonify, request, make_response
from flask import abort, Response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """log in"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/users", methods=["POST"])
def users():
    """register user"""
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
    """welcome"""
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """log out"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """get reset password token"""
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/profile", methods=["GET"])
def profile():
    """profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
