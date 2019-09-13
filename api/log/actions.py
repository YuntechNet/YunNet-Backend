from sanic.response import json
from sanic.blueprints import Blueprint

from Base.MongoDB.actions import query_actions
from Decorators import permission

bp_log_actions = Blueprint("log-actions")

@bp_log_actions.route("/actions/<username>", strict_slashes=True)
@permission("api.log.actions.get")
async def actions_get(request, username):
    result = await query_actions(username)
    print(result)
    return json(result)
