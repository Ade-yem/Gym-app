#!/usr/bin/python3
""" objects that handle all default RestFul API actions for plans """
from models.membership import MembershipPlan
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/plans', methods=['GET'], strict_slashes=False)
def get_plans():
    """
    Retrieves the list of all membership plan objects
    or a specific plan
    """
    all_plans = storage.all(MembershipPlan).values()
    list_plans = []
    for plan in all_plans:
        list_plans.append(plan.to_dict())
    return jsonify(list_plans)


@app_views.route('/plans/<plan_id>', methods=['GET'], strict_slashes=False)
def get_plan(plan_id):
    """ Retrieves a membership plan """
    plan = storage.get(MembershipPlan, plan_id)
    if not plan:
        abort(404)

    return jsonify(plan.to_dict())


@app_views.route('/plans/<plan_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_plan(plan_id):
    """
    Deletes a plan Object
    """

    plan = storage.get(MembershipPlan, plan_id)

    if not plan:
        abort(404)

    storage.delete(plan)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/plans', methods=['POST'], strict_slashes=False)
def post_plan():
    """
    Creates a plan
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = MembershipPlan(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/plans/<plan_id>', methods=['PUT'], strict_slashes=False)
def put_plan(plan_id):
    """
    Updates a Membership plan
    """
    plan = storage.get(MembershipPlan, plan_id)

    if not plan:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(plan, key, value)
    storage.save()
    return make_response(jsonify(plan.to_dict()), 200)
