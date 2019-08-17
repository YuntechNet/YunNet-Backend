from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import api, doc

from Base import messages
from Decorators import permission
from Query.bed import Bed
from Query.group import Group
from Query.ip import Ip
from Query.userinfo import Userinfo

bp_user = Blueprint("user")


class user_info_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            username = doc.String("Username")
            department = doc.String("User's department")
            name = doc.String("User's fullname")
            group = doc.List(doc.String("User's group"))

        model = dict(vars(model))

    class FailResp:
        code = 500
        description = "On failed request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    class AuthResp:
        code = 401
        description = "On failed auth"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp, AuthResp]


@user_info_doc
@bp_user.route("/", methods=["GET"])
@permission("index.userinfo.view")
async def bp_user_info(request, username):
    try:
        user = await Userinfo.get_userinfo(username)
        ip = await Ip.get_user_ip_mac(username)
        bed = await Bed.get_user_bed_info(username)
        group = await Group.get_user_group(username)

        # bed_type = "一般房"
        # if bed["ip_type"] == 1:
        #     bed_type = "晨康房"

        group_list = []
        for g in group:
            group_list.append(g["description"])

        user_obj = {
            "username": user["username"],
            "department": user["department"],
            "name": user["nick"],
            "group": group_list,
        }
        response = json(user_obj)
        return response
    except (TypeError, KeyError):
        logger.warning(request.url + " error occur")
        logger.warning("user:" + str(user))
        logger.warning("ip:" + str(ip))
        logger.warning("bed:" + str(bed))
        logger.warning("group:" + str(group))
        return messages.INTERNAL_SERVER_ERROR
