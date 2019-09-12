from sanic.response import json
from sanic import Blueprint

from Decorators import permission

bp_permission = Blueprint("management-user-permission")


@bp_permission.route("/permission/<username>", methods=["POST"])
@permission("api.permission.get")
async def permission_get(request, username):
    response = json({})
    return response
