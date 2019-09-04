from sanic import Blueprint
from sanic.response import json
from sanic_openapi import api, doc

from Base.types import LockTypes
from Decorators import permission
from Query import Lock

bp_lock = Blueprint("management-lock")


class user_ip_lock_list_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            lock_id = doc.String("lock id")
            lock_type = doc.String("Lock type")
            ip = doc.Integer("ip")
            lock_date = doc.String("Ip's lock date")
            unlock_date = doc.String("Ip's unlock date")
            lock_by_user_id = doc.String("Locked by who")

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


@user_ip_lock_list_doc
@bp_lock.route("/<ip>/lock", methods=["GET"])
@permission("system.dormitory.query.view")
async def bp_user_ip_lock_list(request, ip):
    lock_log = await Lock.get_lock(ip)

    for log in lock_log:
        if log["lock_date"] is not None:
            log["lock_date"] = log["lock_date"].strftime("%Y-%m-%d %H:%M:%S")
        if log["unlock_date"] is not None:
            log["unlock_date"] = log["unlock_date"].strftime("%Y-%m-%d %H:%M:%S")

        lock_type_id = log.pop("lock_type_id")
        if lock_type_id == LockTypes.ABUSE:
            log["lock_type"] = "ABUSE"
        elif lock_type_id == LockTypes.OVERFLOW:
            log["lock_type"] = "OVERFLOW"
        elif lock_type_id == LockTypes.VIRUS:
            log["lock_type"] = "VIRUS"

    return json(lock_log)
