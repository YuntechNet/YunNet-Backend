from sanic.response import json
from sanic import Blueprint

bp_mac = Blueprint("mac")


@bp_mac.route("/<ip>/mac", methods=["GET"])
async def bp_ip_get_owned_ip_mac(request, username, ip):
    response = json()
    return response


@bp_mac.route("/<ip>/mac", methods=["PATCH"])
async def bp_ip_get_owned_ip_mac(request, username, ip):
    response = json()
    return response
