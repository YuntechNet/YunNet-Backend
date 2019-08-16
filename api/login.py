import jwt
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api
from sanic_openapi.doc import JsonBody

from Base.jwt_payload import jwt_payload
from Query.user import User
from Query.permission import Permission
from hashlib import sha256
from Base import messages

bp_login = Blueprint("login")


class user_login_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        recaptcha_token = doc.String("Google RECaptcha token")
        username = doc.String("Username")
        password = doc.String("Password")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On success login"

        class model:
            username = doc.String("Username")
            token = doc.String("User's jwt token")

        model = dict(vars(model))

    class FailResp:
        code = 401
        description = "On failed login"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp]


@user_login_doc
@bp_login.route("/login", methods=["POST"])
async def bp_user_login(request):
    config = request.app.config
    username = request.json["username"]
    password = request.json["password"]
    recaptcha_token = request.json["recaptcha_token"]

    # google reCaptcha verify
    if request.app.config.RECAPTCHA["enabled"]:
        session = request.app.aiohttp_session
        recaptcha_secret = request.app.config.RECAPTCHA["secret"]
        data = {"secret": recaptcha_secret, "response": recaptcha_token}
        async with session.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        ) as resp:
            resp_json = await resp.json()
            if not resp_json["success"]:
                return messages.RECAPTCHA_FAILED

    # check login permission
    allowed = await Permission.check_permission(username, "index.login.login")

    if not allowed:
        return messages.NO_PERMISSION

    encode_password = (password + config.PASSWORD_SALT).encode("UTF-8")
    hashed_password = sha256(encode_password).hexdigest()
    db_pw = await User.get_password(username)

    if db_pw != hashed_password:
        return messages.LOGIN_FAILED
    token = jwt.encode(
        jwt_payload(username), config.JWT["jwtSecret"], config.JWT["algorithm"]
    ).decode("utf-8")

    resp = json({"username": username, "token": token}, 200)
    return resp
