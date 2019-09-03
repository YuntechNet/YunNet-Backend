from sanic.log import logger
from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc

from Query.ip import Ip

bp_ip = Blueprint("management-ip", url_prefix="/ip")


# @doc.summary("Query IP managed by the switch")
# @doc.consumes(
#     doc.JsonBody({"switch": str, "mode": int, "status": int}),  # optional  # optional
#     content_type="application/json",
#     location="body",
# )
# @doc.produces(
#     [
#         {
#             "ip": str,
#             "status": int,
#             "mac": str,
#             "update": int,
#             "port": int,
#             "port_type": int,
#             "switch": str,
#         }
#     ],
#     content_type="application/json",
# )
# @bp_ip.route("/", methods=["GET", "POST"])
# def ip_get(request):
#     try:
#         switch = request.json["switch"]
#         mode = request.json.get("mode", None)
#         status = request.json.get("status", None)
#         data = Ip().get_ip_by_switch(switch)
#
#         if mode is not None:
#             data = tuple(filter(lambda x: x["status"] == mode, data))
#         if status is not None:
#             data = tuple(filter(lambda x: x["update"] == status, data))
#     except Exception as e:
#         logger.warning(e)
#     return json(data)


# @doc.summary('Update IP mode and status')
# @doc.consumes(
#     doc.JsonBody(
#         [
#             {
#                 "ip": str,
#                 "mode": int,
#                 "status": int
#             }
#         ]
#     ), content_type="application/json", location="body"
# )
# @bp_ip.route("/", methods=["PATCH"])
# def ip_post(request: Request):
#     return json({})
