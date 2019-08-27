from sanic_openapi import doc, api

from Base import messages
from .login import bp_login


class forgot_password_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        username = doc.String("Username")
        email = doc.String("User's email")

    consumes = doc.JsonBody(vars(consumes))

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


@forgot_password_doc
@bp_login.route("/forgot-password", methods=["POST"])
async def bp_user_forgot_password(request):
    username = request.json["username"]
    email = request.json["email"]
    # TODO recover jwt token

    # TODO send recover token
    return messages.SERVICE_UNAVAILABLE


@bp_login.route("/forgot-password/<token>", methods=["GET"])
async def bp_user_forgot_password_verify(request, token):
    # TODO verify token and remove from db
    return messages.SERVICE_UNAVAILABLE
