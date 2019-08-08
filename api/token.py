import jwt
from pymysql import MySQLError
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc

import config
from Base import messages
from Base.jwt_payload import jwt_payload
from Query.bed import Bed
from Query.user import User
from Query.permission import Permission
from hashlib import sha256

from Query.userinfo import Userinfo

bp_token = Blueprint("token")


@bp_token.route("/login", methods=["POST"], strict_slashes=True)
@doc.consumes(
    doc.JsonBody({"recaptcha_token": str, "username": str, "password": str}),
    content_type="application/json",
    location="body",
)
async def bp_login(request):
    # try:
    username = request.json["username"]
    password = request.json["password"]
    recaptcha_token = request.json["recaptcha_token"]

    # google reCaptcha verify
    # only check debug = false
    if not request.app.debug:
        session = request.app.aiohttp_session
        recaptcha_secret = request.app.config.RECAPTCHA["secret"]
        data = {"secret": recaptcha_secret, "response": recaptcha_token}
        async with session.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        ) as resp:
            resp_json = await resp.json()
            if not resp_json["success"]:
                return json({"message": "token verify failed"})

    # check login permission
    allowed = await Permission().check_permission(username, "index.login.login")

    if not allowed:
        return json({"message": "no permission"}, 403)

    encode_password = (password + config.PASSWORD_SALT).encode("UTF-8")
    hashed_password = sha256(encode_password).hexdigest()
    db_pw = await User().get_password(username)

    logger.debug(db_pw)
    logger.debug(hashed_password)
    if db_pw != hashed_password:
        return json({"message": "Username/Password combination incorrect"}, 401)
    token = jwt.encode(
        jwt_payload(username), config.JWT["jwtSecret"], config.JWT["algorithm"]
    ).decode("utf-8")

    resp = json({"username": username, "token": token}, 200)
    return resp
    # except KeyError as e:
    #     logger.warning(e)
    #     return json({'message': 'Username/Password combination incorrect'},
    #                 401)


# a.k.a. account activate
@bp_token.route("/register", methods=["POST"], strict_slashes=True)
@doc.consumes(
    doc.JsonBody({"id": str, "bed": str}),
    content_type="application/json",
    location="body",
    required=True,
)
async def bp_register(request):
    # 0200 -> 0300

    id = request.json["id"]
    bed = request.json["bed"]
    user_bed = await Bed().get_user_bed_info(id)

    if user_bed is None:
        return json(messages.NO_PERMISSION, 400)

    logger.warning(user_bed)

    if user_bed["bed"] == bed:
        if await User().set_group(id, 3):
            resp = json({"message": "register complete"}, 200)
        else:
            resp = json({"message": "register fail"}, 500)
    else:
        resp = json({"message": "wrong bed_id or id"}, 400)

    return resp
