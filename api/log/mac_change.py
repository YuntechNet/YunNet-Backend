from sanic.response import json
from sanic import Blueprint

from Base.MongoDB.mac import query_mac_change_by_ip, query_mac_change_by_owner
from Decorators import permission
from documentation.log.mac_change_doc import (
    MacChangeGetLogByUsernameDoc,
    MacChangeGetLogByIpDoc,
)

bp_log_mac = Blueprint("log-mac")


@MacChangeGetLogByUsernameDoc
@bp_log_mac.route("/mac/<username>", strict_slashes=True)
@permission("api.log.mac.get")
async def mac_get_by_owner(request, username):
    result = await query_mac_change_by_owner(username)
    return json(result)


@MacChangeGetLogByIpDoc
@bp_log_mac.route("/ip/mac/<ip>", strict_slashes=True)
@permission("api.log.mac.get")
async def mac_get_by_ip(request, ip):
    result = await query_mac_change_by_ip(ip)
    return json(result)
