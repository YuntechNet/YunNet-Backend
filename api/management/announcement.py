from sanic.response import json
from sanic import Blueprint

announcement = Blueprint("management-announcement", url_prefix="/announcement")

# TODO(biboy1999): Low priority
# @announcement.route("/", methods=["GET"])
# async def bp_get(request):
#     response = json({})
#     return response
#
#
# @announcement.route("/", methods=["POST"])
# async def bp_add(request):
#     # return content-location(post_id)
#     response = json({})
#     return response
#
#
# @announcement.route("/<post_id>", methods=["PUT"])
# async def bp_edit(request, post_id):
#     response = json({})
#     return response
#
#
# @announcement.route("/<post_id>", methods=["DELETE"])
# async def bp_delete(request, post_id):
#     response = json({})
#     return response
