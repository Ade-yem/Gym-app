#!/usr/bin/env python3
"""Auth view module"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.users import User
from api.v1.app import auth


@app_views.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """handle registration"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON missing"}), 400
    

@app_views.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """handle login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    if auth.check_login(email, password):
        session_id = auth.create_session(email)
        if not session_id:
            abort(401)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)

@app_views.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """handle logout"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    auth.destroy_session(session_id)
    return jsonify({}), 200