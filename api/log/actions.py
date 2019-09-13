from sanic.response import json
from sanic.blueprints import Blueprint

from Base import messages
from Base.MongoDB.actions import query_actions
from Decorators import permission
from Query import Permission
from documentation.log.actions_doc import ActionGetLogDoc

bp_log_actions = Blueprint("log-actions")


@ActionGetLogDoc
@bp_log_actions.route("/actions/<username>", strict_slashes=True)
@permission("api.log.actions.get")
async def actions_get(request, username):
    if request["username"] != username:
        if not await Permission.check_permission(
            request["username"], "api.log.actions.all"
        ):
            return messages.NO_PERMISSION
    result = await query_actions(username)
    print(result)
    return json(result)
