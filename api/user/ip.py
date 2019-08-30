from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api

from Base import types
from Base.types import IpTypes, IpStatus
from Decorators import permission
from Query.ip import Ip
from Query import Lock

bp_ip = Blueprint("ip")


class user_ip_get_own_ip_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            ip = doc.String("Ip")
            mac = doc.String("MAC address of an IP")
            is_updated = doc.Integer("if MAC is updated to switch")
            description = doc.String("IP description")
            locked = doc.String("If a IP is locked")

        model = doc.List(model)

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


@user_ip_get_own_ip_doc
@bp_ip.route("/ip", methods=["GET"])
@permission("index.userinfo.view")
async def bp_ip_get_owned_ip(request, username):
    ips = await Ip.get_user_own_ip(username)

    remove_key_list = [
        "switch_id",
        "ip_type_id",
        "port",
        "port_type",
        "uid",
        "gid",
    ]

    for ip in ips:
        for key in remove_key_list:
            ip.pop(key)

        lock_id = ip.pop("lock_id")
        if lock_id is None:
            ip["locked"] = False
        else:
            ip["locked"] = True
            lock = await Lock.get_lock_by_id(lock_id)
            ip["lock_reason"] = lock["description"]

        if not bool(int(ip["is_unlimited"])):
            ip.pop("is_unlimited")
        else:
            ip["is_unlimited"] = True

    response = json(ips)
    return response
