from sanic.request import Request
from sanic.response import json
from sanic import Blueprint
from sanic.log import logger
from datetime import datetime
from sanic_openapi import doc, api
from sanic_openapi.doc import JsonBody
import asyncio

import config
from Base import messages
from Base.types import LockTypes
from Query import Lock, User
from Decorators import permission
from BackgroundJobs import switch_update

bp_abuse = Blueprint("management-abuse")


class abuse_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        reason = doc.String("reason")
        lock_until = doc.Date("YYYY-MM-DD")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On request succeded"

        class model:
            message = doc.String("OPERATION_SUCCESS")

        model = dict(vars(model))

    class FailResp:
        code = 400
        description = "On failed request"

        class model:
            message = doc.String("BAD_REQUEST")

        model = dict(vars(model))

    class ServerFailResp:
        code = 500
        description = "When server failed to process the response"

        class model:
            message = doc.String("INTERNAL_SERVER_ERROR")

        model = dict(vars(model))

    class AuthResp:
        code = 401
        description = "On failed auth"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, ServerFailResp, AuthResp]


@abuse_doc
@bp_abuse.route("/abuse/<ip>", methods=["PUT"], strict_slashes=True)
@permission("system.universal.abuse.lock")
async def bp_abuse_put(request: Request, ip):
    try:
        title = request.json["title"]
        description = request.json["description"]
        lock_until_str = request.json["lock_until"]
        lock_until = None

        if lock_until_str is not None:
            lock_until = datetime.strptime(lock_until_str, "%Y-%m-%d")
        locked_by = await User.get_user_id(request["username"])

    except Exception as e:
        logger.debug(e.with_traceback())
        return messages.BAD_REQUEST
    
    await Lock.set_lock(ip, 1, datetime.now(), lock_until, title, description, locked_by)
    app_config: config = request.app.config
    asyncio.create_task(switch_update(app_config.API_ENDPOINT))
    return messages.ACCEPTED
