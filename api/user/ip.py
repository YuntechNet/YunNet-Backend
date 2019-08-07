from sanic.response import json
from sanic import Blueprint

bp_ip = Blueprint("ip")


@bp_ip.route("/ip", methods=["GET"])
async def bp_ip_get_owned_ip(request, uid):
    body = [
        {
            "ip": "140.125.200.200",
            "mac": "",
            "is_updated": True,
            "is_locked": False,
            "type": 0,
        }
    ]
    response = json(body)
    return response
