from sanic.response import json
from sanic import Blueprint
from sanic_openapi import api, doc

from Base import messages
from Query import User
from Query.userinfo import Userinfo

bp_user_manage = Blueprint("management-user-manage")


# @bp_user_manage.route("/<username>", methods=["POST"])
# async def bp_add_user(request, username):
#     pass


# TODO(biboy1999): Low priority
# @manage.route("/<username>", methods=["PUT"])
# async def bp_edit(request, username):
#     response = json({})
#     return response


# @bp_user_manage.route("/<username>", methods=["DELETE"])
# async def bp_delete(request, username):
#     pass
