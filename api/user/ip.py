from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api

from Base import types
from Base.types import IpTypes, IpStatus
from Decorators import permission
from Query.ip import Ip

bp_ip = Blueprint("ip")


class user_ip_get_own_ip_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            ip = doc.String("Ip")
            mac = doc.String("Ip's mac address")
            is_updated = doc.Integer("Is updated to switch")
            description = doc.String("Ip's description")
            lock_status = doc.String("Ip's lock status")

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
async def bp_ip_get_owned_ip(request, username):
    ips = await Ip.get_user_own_ip(username)

    remove_key_list = [
        "switch_id",
        # "status_id",
        "ip_type_id",
        "port",
        "port_type",
        "uid",
        "gid",
    ]
    for ip in ips:
        for key in remove_key_list:
            ip.pop(key)
        status_id = ip.pop("status_id")
        if status_id == IpStatus.UNLOCK:
            ip["lock_status"] = "未鎖定"
        elif status_id == IpStatus.LOCK:
            ip["lock_status"] = "鎖定"
        elif status_id == IpStatus.UNLIMITED:
            ip["lock_status"] = "無限制"

    response = json(ips)
    return response
