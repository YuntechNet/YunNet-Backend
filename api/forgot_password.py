from datetime import time, timedelta, datetime
from hashlib import sha256

from sanic import Blueprint
from sanic_openapi import doc, api
from email.mime.text import MIMEText

from Base import messages, SMTP
from Base import messages
from Query import User
from Query.token import Token

bp_forgot_passowrd = Blueprint("forgot-password")


class forgot_password_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        username = doc.String("Username")

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
@bp_forgot_passowrd.route("/forgot-password", methods=["POST"])
async def bp_user_forgot_password(request):
    username = request.json["username"]
    # TODO recover jwt token
    content = (
        "請點擊下方連結重置您的密碼：\n"
        "https://yunnet.yuntech.com.tw/#/verify?={0}\n"
        "\n"
        "Please click following link to reset your password:\n"
        "https://yunnet.yuntech.com.tw/#/verify?={0}\n"
        "\n"
    )
    # Token creation
    hexdigest = username + repr(time())
    hexdigest = sha256(hexdigest.encode()).hexdigest()
    recover_code = username + "_" + hexdigest

    # Insert to database
    uid = await User.get_user_id(username)
    affect_row = await Token.add_token(uid, recover_code)
    if not affect_row:
        return messages.INTERNAL_SERVER_ERROR

    # Send mail
    mail = MIMEText(content.format(recover_code), "plain", "utf-8")
    mail["From"] = SMTP.sender
    mail["To"] = username + "@yuntech.edu.tw"
    mail["Subject"] = "YunNet 密碼重置"
    await SMTP.send_message(mail)

    resp = messages.OPERATION_SUCCESS

    return resp


class forgot_password_verify_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        password = doc.String("User's new password")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 202
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


@forgot_password_verify_doc
@bp_forgot_passowrd.route("/forgot-password/<token>", methods=["POST"])
async def bp_user_forgot_password_verify(request, token):
    # TODO verify token and remove from db
    username = token.split("_")[0]
    password = request.json["password"]
    db_token = await Token.get_token(token)

    if db_token in None:
        return messages.INVALID_TOKEN

    # token only live 1 hour
    delta= datetime.now() - db_token["timestamp"]
    if delta > timedelta(hours=1):
        await Token.delete_token(token)
        return messages.TOKEN_EXPIRED

    # Set user password
    op_success = await User.set_password(username, password)
    if not op_success:
        return messages.INTERNAL_SERVER_ERROR

    # Operation success
    await Token.delete_token(token)

    return messages.PASSWORD_SUCCESSFULLY_CHANGED
