from sanic.log import logger
from sanic.response import json
from sanic_openapi import doc, api

from Base import messages
from Query import User
from Query.bed import Bed
from Query.group import Group

from .login import bp_login


class user_register_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        username = doc.String("Username")
        bed = doc.String("User's bed number")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On success register"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    class FailResp:
        code = 401
        description = "On failed register"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    class InteralFailResp:
        code = 500
        description = "On Server-side failed register"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, InteralFailResp]


# a.k.a. account activate
@user_register_doc
@bp_login.route("/register", methods=["POST"])
async def bp_register(request):
    username = request.json["username"]
    bed = request.json["bed"]
    user_bed = await Bed.get_user_bed_info(username)

    if user_bed is None:
        return messages.NO_PERMISSION

    group_list = await Group.get_user_group(username)
    if any(group["gid"] == 3 for group in group_list):
        return messages.REGISTER_ALREADY

    if user_bed["bed"] == bed:
        await Group.remove_user_group(username, 2)
        if await Group.add_user_group(username, 3):
            resp = messages.REGISTER_SUCCESS
        else:
            resp = messages.INTERNAL_SERVER_ERROR
    else:
        resp = messages.REGISTER_FAIL

    return resp
