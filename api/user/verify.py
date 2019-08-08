from sanic.response import json
from sanic import Blueprint
from Base import messages

bp_verify = Blueprint("verify")


@bp_verify.route("/verify/{token}", methods=["GET"])
async def bp_verify_mail(request):
    return messages.ACTIVATION_SUCCESS
