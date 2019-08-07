from sanic.response import json
from sanic import Blueprint

from Query.bed import Bed
from Query.ip import Ip
from Query.userinfo import Userinfo

bp_user = Blueprint("user")


@bp_user.route("/", methods=["GET"])
async def bp_user_info(request, uid):
    # user_obj = {'user': 'B11078763',
    #             'department': '四資工一A',
    #             'name': '陳凱文',
    #             'ip': '8.8.8.8',
    #             'mac': 'FF:FF:FF:FF',
    #             'portal': 'C871',
    #             'bed': 'C876-3',
    #             'bed_type': '一般房',
    #             'status': '已使用/已註冊'
    #             }
    user = Userinfo().get_userinfo(uid)
    ip = Ip().get_user_ip_mac(uid)
    bed = Bed().get_user_bed_info(uid)

    user_obj = {
        "user": user.get("username", None),
        "department": user.get("department", None),
        "name": user.get("nick", None),
        "ip": ip.get("ip"),
        "mac": ip.get("mac"),
        "portal": bed.get("portal"),
        "bed": bed.get("bed"),
        "bed_type": "一般房",
        "status": "已使用/已註冊",
    }

    response = json(user_obj)
    return response
