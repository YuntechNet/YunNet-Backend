from sanic.response import json
from sanic import Blueprint
from sanic_openapi import api, doc

from Base import messages
from Query import User
from Query.userinfo import Userinfo

manage = Blueprint("management-user-manage")


class add_user_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        username = doc.String("Username")
        nick = doc.String("User's name")
        department = doc.String("User's department")
        back_mail = doc.String("User's backup mail")
        note = doc.String("Additional note")

    consumes = doc.JsonBody(vars(consumes))

    class SuccessResp:
        code = 200
        description = "On success login"

        class model:
            username = doc.String("Username")
            token = doc.String("User's jwt token")

        model = dict(vars(model))

    class FailResp:
        code = 400
        description = "On failed login"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp]


@add_user_doc
@manage.route("/<username>", methods=["POST"])
async def bp_add_user(request, username):
    user = await Userinfo.get_userinfo(username)
    if user is not None:
        return messages.USER_ALREADY_EXIST

    username = request.json["username"]
    nick = request.json["nick"]
    department = request.json["department"]
    back_mail = request.json["back_mail"]
    note = request.json["note"]

    affected = await User.add_user(username, nick, department, back_mail, note)
    if affected == 0:
        return messages.INTERNAL_SERVER_ERROR
    return messages.OPERATION_SUCCESS


# TODO(biboy1999): Low priority
# @manage.route("/<username>", methods=["PUT"])
# async def bp_edit(request, username):
#     response = json({})
#     return response


class delete_user_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success login"

        class model:
            username = doc.String("Username")
            token = doc.String("User's jwt token")

        model = dict(vars(model))

    class FailResp:
        code = 400
        description = "On failed login"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp]


@delete_user_doc
@manage.route("/<username>", methods=["DELETE"])
async def bp_delete(request, username):
    user = await Userinfo.get_userinfo(username)
    if user is not None:
        return messages.USER_NOT_EXIST

    await User.delete_user(username)

    return messages.OPERATION_SUCCESS
