from sanic.response import json
from sanic.blueprints import Blueprint

from Base.MongoDB.lock import query_lock_by_ip, query_lock_by_owner
from Decorators import permission
from documentation.log.lock_doc import LockGetLogByUsernameDoc, LockGetLogByIpDoc

bp_log_lock = Blueprint("log-lock")


@LockGetLogByUsernameDoc
@bp_log_lock.route("/lock/<username>", strict_slashes=True)
@permission("api.log.lock.get")
async def lock_get_by_owner(request, username):
    result = await query_lock_by_owner(username)
    return json(result)


@LockGetLogByIpDoc
@bp_log_lock.route("/ip/lock/<ip>", strict_slashes=True)
@permission("api.log.lock.get")
async def actions_get_by_ip(request, ip):
    result = await query_lock_by_ip(ip)
    return json(result)
