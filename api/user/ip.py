from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc

from Query.ip import Ip

bp_ip = Blueprint("ip")


@bp_ip.route("/ip", methods=["GET"], strict_slashes=True)
@doc.produces(
    [{"ip": str, "mac": str, "is_updated": bool, "description": str}],
    content_type="application/json",
)
async def bp_ip_get_owned_ip(request, username):
    ips = await Ip.get_user_own_ip(username)

    remove_key_list = [
        "switch_id",
        "status_id",
        "ip_type_id",
        "port",
        "port_type",
        "uid",
        "gid",
    ]
    for ip in ips:
        for key in remove_key_list:
            ip.pop(key)

    response = json(ips)
    return response
