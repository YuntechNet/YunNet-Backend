from sanic.response import json
from sanic import Blueprint

manage = Blueprint("management-user-manage", url_prefix="/<user_id>")


# user's permission management
@manage.route("/permission", methods=["GET"])
async def bp_list_permission(request, user_id):
    response = json({})
    return response


@manage.route("/permission/<code>", methods=["POST"])
async def bp_add_permission(request, user_id, code):
    response = json({})
    return response


@manage.route("/permission/<code>", methods=["DELETE"])
async def bp_remove_permission(request, user_id, code):
    response = json({})
    return response


@manage.route("/", methods=["POST"])
async def bp_add(request, user_id):
    # return content-location
    response = json({})
    return response


@manage.route("/", methods=["PUT"])
async def bp_delete(request, user_id):
    response = json({})
    return response


@manage.route("/", methods=["DELETE"])
async def bp_delete(request, user_id):
    response = json({})
    return response
