import jwt
from pymysql import MySQLError
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc

import config
from Base.jwt_payload import jwt_payload
from Query.user import User
from Query.permission import Permission
from hashlib import sha256

from Query.userinfo import Userinfo

bp_token = Blueprint("token")


@bp_token.route("/login", methods=["POST"])
@doc.consumes(
    doc.JsonBody({"recaptcha_token": str, "username": str, "password": str}),
    content_type="application/json",
    location="body",
)
async def bp_login(request):
    try:
        username = request.json["username"]
        password = request.json["password"]
        recaptcha_token = request.json["recaptcha_token"]
        # google reCaptcha verify
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
        allowed = Permission().check_permission(username, "4701")

        if not allowed:
            return json({"message": "no permission"}, 403)

        encode_password = (password + config.PASSWORD_SALT).encode("UTF-8")
        hashed_password = sha256(encode_password).hexdigest()
        db_pw = User().get_password(username)

        if db_pw != hashed_password:
            return json({"message": "Username/Password combination incorrect"}, 401)
        token = jwt.encode(
            jwt_payload(username), config.JWT["jwtSecret"], config.JWT["algorithm"]
        )

        resp = json({"username": username, "token": token}, 200)

    except KeyError as e:
        return json({"message": "Username/Password combination incorrect"}, 401)
    except MySQLError as e:
        logger.error("Catch MySQLError:{}".format(e.args[1]))
        return json("messages.INTERNAL_SERVER_ERROR", 500)
    return resp


# a.k.a. account activate
@bp_token.route("/register", methods=["POST"])
@doc.consumes(
    doc.JsonBody({"id": str, "bed": str}),
    content_type="application/json",
    location="body",
    required=True,
)
async def bp_register(request):
    # 0200 -> 0300
    try:
        id = request.json["id"]
        bed = request.json["bed"]
        userinfo = Userinfo().get_userinfo(id)
    except KeyError:
        return json({"message": "bad request"}, 400)
    except MySQLError as e:
        logger.error("Catch MySQLError:{}".format(e.args[1]))
        return json("messages.INTERNAL_SERVER_ERROR", 500)

    if userinfo is None:
        return json({"message": "id not found"}, 400)

    if userinfo["bed_id"] == bed:
        if User().set_group(id, "0300"):
            resp = json({"message": "register complete"}, 200)
        else:
            resp = json({"message": "register fail"}, 500)
    else:
        resp = json({"message": "wrong bed_id or id"}, 400)

    return resp
