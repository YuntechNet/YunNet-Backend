from sanic.response import json
from sanic import Blueprint

bp_bed = Blueprint("bed")


@bp_bed.route("/bed", methods=["GET"])
async def bp_user_info(request, uid):
    response = json()
    return response
