from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api
from datetime import datetime, timedelta

from Base import messages
from Query.group import Group
from Query.token import Token
from Query.user import User
from documentation.verify_mail_doc import VerifyMailDoc

bp_verify_mail = Blueprint("verify-mail")


@VerifyMailDoc
@bp_verify_mail.route("/verify-mail/<token>", methods=["GET"])
async def verify_mail(request, token):
    db_token = await Token.get_token(token)

    if db_token is None:
        return messages.INVALID_TOKEN

    # token only live 1 hour
    delta: timedelta = datetime.now() - db_token["timestamp"]
    if delta > timedelta(hours=1):
        await Token.delete_token(token)
        return messages.TOKEN_EXPIRED

    # switch user's group
    username = await User.get_username(db_token["uid"])
    await Group.remove_user_group(username, 2)
    if await Group.add_user_group(username, 3):
        await Token.delete_token(token)
        return messages.ACTIVATION_SUCCESS
    else:
        return messages.INTERNAL_SERVER_ERROR
