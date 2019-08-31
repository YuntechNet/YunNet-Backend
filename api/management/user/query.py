from sanic.response import json
from sanic import Blueprint
from sanic_openapi import api, doc

from Base import messages
from Decorators import permission
from Query.group import Group
from Query.ip import Ip
from Query.userinfo import Userinfo

import re

bp_query = Blueprint("management-user-query")


class user_query_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            users = doc.List(
                {
                    "uid": int,
                    "username": str,
                    "name": str,
                    "department": str,
                    "group": [],
                }
            )
            ip = doc.List(
                {
                    "ip": str,
                    "ip_type_id": int,
                    "is_unlimited": bool,
                    "switch_id": int,
                    "port": int,
                    "port_type": str,
                    "mac": str,
                    "is_updated": bool,
                    "description": str,
                }
            )

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


@user_query_doc
@bp_query.route("/<query>", methods=["GET"])
@permission("system.dormitory.query.query")
async def bp_user_query(request, query):
    # TODO(biboy1999): will refactor later

    def ip_list_wraper(ip_list):
        for ip in ip_list:
            ip.pop("uid")
            ip.pop("gid")

            status = ip.get("lock_id", None)
            if status is None:
                ip["lock_status"] = "UNLOCKED"

                status = ip.get("is_unlimited", None)
                if status == 1:
                    ip["lock_status"] = "UNLIMITED"

            else:
                ip["lock_status"] = "LOCKED"

        return ip_list

    resp = {"user": [], "ip": []}
    group_list = []

    ip_regex = "^(?:(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$"
    bed_regex = "^[A-Za-z][0-9]{4}-[0-9]$"

    if re.search(ip_regex, query) is not None:
        mode = "ip"
        user = await Userinfo.get_fullinfo(query, mode)

        if user is None:
            ip = await Ip.get_ip_by_id(query)
            resp["ip"] = ip
            return json(resp)

        user.pop("password_hash")

        ip_list = await Ip.get_user_own_ip(user["username"])
        if ip_list is not None:
            ip_list = ip_list_wraper(ip_list)

        group = await Group.get_user_group(user["username"])
        for g in group:
            group_list.append(g["description"])

        user["group"] = group_list
        resp["user"] = user
        resp["ip"] = ip_list

    elif re.search(bed_regex, query.upper()) is not None:
        mode = "bed"
        user = await Userinfo.get_fullinfo(query, mode)
        if user is None:
            ip = await Ip.get_ip_by_bed(query)
            resp["ip"] = ip
            return json(resp)

        user.pop("password_hash")

        ip_list = await Ip.get_user_own_ip(user["username"])
        if ip_list is not None:
            ip_list = ip_list_wraper(ip_list)

        group = await Group.get_user_group(user["username"])
        for g in group:
            group_list.append(g["description"])
        user["group"] = group_list
        resp["user"] = user
        resp["ip"] = ip_list

    else:
        mode = "username"
        user = await Userinfo.get_fullinfo(query, mode)
        if user is not None:

            user.pop("password_hash")

            ip_list = await Ip.get_user_own_ip(user["username"])
            if ip_list is not None:
                ip_list = ip_list_wraper(ip_list)

            group = await Group.get_user_group(user["username"])
            for g in group:
                group_list.append(g["description"])
            user["group"] = group_list
            resp["user"] = user
            resp["ip"] = ip_list

    return json(resp)
