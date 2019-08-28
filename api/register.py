from sanic.log import logger
from sanic.response import json
from sanic_openapi import doc, api
from email.mime.text import MIMEText
from hashlib import sha256
from time import time

from Base import messages, SMTP
from Query.user import User
from Query.bed import Bed
from Query.group import Group
from Query.token import Token

from .login import bp_login


class user_register_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        username = doc.String("Username")
        bed = doc.String("User's bed number")
        password = doc.String("User's password")

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
    config = request.app.config
    username = request.json["username"]
    bed = request.json["bed"]
    password = request.json["password"]

    user_bed = await Bed.get_user_bed_info(username)
    group_list = await Group.get_user_group(username)

    if user_bed is None:
        return messages.NO_PERMISSION

    if any(group["gid"] == 3 for group in group_list):
        return messages.ALREADY_REGISTERED

    if user_bed["bed"] == bed:
        # Activation mail content
        content = (
            "請點擊下方連結驗證您的帳號：\n"
            "https://yunnet.yuntech.com.tw/#/register_verify/{0}\n"
            "\n"
            "Please click following link to activate your account:\n"
            "https://yunnet.yuntech.com.tw/#/register_verify/{0}\n"
            "\n"
            "\n"
            "如須設定網路教學，請點擊下方連結（中文版）：\n"
            "MISSING_URL\n"
            "\n"
            "If you need instruction on configuring internet, please click the following link (English):\n"
            "MISSING_URL\n"
        )
        # Token creation
        hexdigest = username + repr(time())
        hexdigest = sha256(hexdigest.encode()).hexdigest()
        activation_code = username + "_" + hexdigest

        # Send mail
        mail = MIMEText(content.format(activation_code), "plain", "utf-8")
        mail["From"] = SMTP.sender
        mail["To"] = username + "@yuntech.edu.tw"
        mail["Subject"] = "YunNet 驗證帳號"
        await SMTP.send_message(mail)
        resp = messages.REGISTER_SUCCESS

        # Insert to database
        uid = await User.get_user_id(username)
        affect_row = await Token.add_token(uid, activation_code)
        if not affect_row:
            return messages.INTERNAL_SERVER_ERROR

        # Set user password
        encode_password = (password + config.PASSWORD_SALT).encode("UTF-8")
        hashed_password = sha256(encode_password).hexdigest()
        op_success = await User.set_password(username, hashed_password)
        if not op_success:
            return messages.INTERNAL_SERVER_ERROR

    else:
        resp = messages.REGISTER_FAIL

    return resp
