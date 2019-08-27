from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api

from Base import messages
from Query.group import Group
from Query.token import Token
from Query.user import User

bp_verify_mail = Blueprint("verify-mail")


class verify_mail_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            message = doc.String("message")

        model = dict(vars(model))

    class FailResp:
        code = 401
        description = "On failed request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp]


@verify_mail_doc
@bp_verify_mail.route("/verify-mail/<token>", methods=["GET"])
async def verify_mail(request, token):
    db_token = await Token.get_token(token)

    if db_token is None:
        return messages.ACTIVATION_FAILED

    username = await User.get_username(db_token["uid"])

    await Group.remove_user_group(username, 2)
    if await Group.add_user_group(username, 3):
        return messages.ACTIVATION_SUCCESS
    else:
        return messages.INTERNAL_SERVER_ERROR
