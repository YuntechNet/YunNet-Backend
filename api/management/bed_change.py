from sanic import Blueprint
from sanic_openapi import api, doc

from Base import messages
from Decorators import permission
from Query.bed import Bed
from Query.ip import Ip

bp_bed_change = Blueprint("management-bed-change")


class change_bed_doc(api.API):
    consumes_content_type = "application/json"
    consumes_location = "body"
    consumes_required = True

    class consumes:
        source_bed = doc.String("Source bed")
        # source_username = doc.String("Source user")
        dest_bed = doc.String("Destination bed")
        # dest_username = doc.String("Destination user")

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

    response = [SuccessResp, FailResp]

@change_bed_doc
@bp_bed_change.route("/", methods=["POST"])
@permission("system.dormitory.bed.exchange")
async def change_bed(request):
    source_bed = request.json["source_bed"]
    dest_bed = request.json["dest_bed"]
    # for validate uid
    # source_username = request.json["source_username"]
    # dest_username = request.json["dest_username"]

    source_ip = await Ip.get_ip_by_bed(source_bed)
    dest_ip = await Ip.get_ip_by_bed(dest_bed)

    if source_ip is None or dest_ip is None:
        return messages.BAD_REQUEST
    source_uid = source_ip[0]["uid"]
    dest_uid = dest_ip[0]["uid"]

    await Ip.assign_user(dest_ip[0]["ip"], source_uid)
    await Ip.assign_user(source_ip[0]["ip"], dest_uid)

    return messages.OPERATION_SUCCESS
