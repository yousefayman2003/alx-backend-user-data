#!/usr/bin/env python3
""" Module of session auth views
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return:
     - User instance based on email
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for u in users:
        if not u.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(u.id)
        response = jsonify(u.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)
        return response
    return jsonify({"error": "no user found for this email"}), 404


    @app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
    def logout():
        """ DELETE /auth_session/logout
        Return:
         - Empty dictionary if successful
        """
        from api.v1.app import auth
        if not auth.destroy_session(request):
            return abort(404)
        return jsonify({}), 200
