from sanic.response import json
from sanic import Blueprint
from Base import messages

bp_verify_mail = Blueprint("verify-mail")


@bp_verify_mail.route("/verify-mail/<token>", methods=["GET"])
async def verify_mail(request, token):
    return messages.ACTIVATION_SUCCESS
