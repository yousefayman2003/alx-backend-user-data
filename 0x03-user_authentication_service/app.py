#!/usr/bin/env python3
"""
Module to create a Flask app
"""

from flask import Flask, jsonify, Response, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """GET route index

    Returns:
        str: json {'message': 'Bienvenue'}
    """
    message = {"message": "Bienvenue"}

    return jsonify(message)

@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Handles user registration via POST request.

    Returns:
        str: A message indicating the outcome of the registration attempt.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400





if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
