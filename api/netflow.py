from sanic.response import json
from sanic import Blueprint

from Decorators import permission

bp_netflow = Blueprint("netflow")


# TODO(biboy1999): filter for paging or datetime
@bp_netflow.route("/netflow/<ip>", methods=["GET"])
@permission("system.debug")
async def bp_netflow_offset(request, ip):
    netflow_data = {}
    response = json(netflow_data)
    return response


# @netflow.route('/netflow/<offset>', methods=['GET'])
# async def bp_netflow(request, offset):
#     response = json()
#     return response
