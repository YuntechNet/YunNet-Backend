from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api
from hashlib import sha256

from Base import messages
from Decorators import permission
from Query import User

bp_password = Blueprint("password")


class user_set_owned_ip_mac_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        old_password = doc.String("Old password")
        new_password = doc.String("New Password")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            message = doc.String("Message")

        model = dict(vars(model))

    class FailResp:
        code = 500
        description = "On failed request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    class AuthResp:
        code = 401
        description = "On failed Auth"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, AuthResp]


@user_set_owned_ip_mac_doc
@bp_password.route("/password", methods=["PATCH"])
@permission("index.userinfo.change_passwd.view")
async def bp_user_change_password(request, username):
    config = request.app.config
    username = request.args["token_username"]
    old_password_raw = request.json["old_password"]
    new_password_raw = request.json["new_password"]

    old_password_encoded = (old_password_raw + config.PASSWORD_SALT).encode("UTF-8")
    new_password_encoded = (new_password_raw + config.PASSWORD_SALT).encode("UTF-8")

    old_password_hashed = sha256(old_password_encoded).hexdigest()
    new_passowrd_hashed = sha256(new_password_encoded).hexdigest()

    db_password = await User.get_password(username)

    if db_password != old_password_hashed:
        return messages.PASSWORD_NOT_MATCH

    if await User.set_password(username, new_passowrd_hashed):
        return messages.OPERATION_SUCCESS
    else:
        return messages.INTERNAL_SERVER_ERROR
