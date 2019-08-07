from sanic.response import json
from sanic import Blueprint

bp_department = Blueprint("department")


@bp_department.route("/department", methods=["GET"])
async def bp_user_info(request, uid):
    response = json()
    return response
