from sanic.response import json
from sanic import Blueprint

bp_ip = Blueprint('ip')


@bp_ip.route('/ip', methods=['GET'])
async def bp_ip_get_owned_ip(request, uid):
    response = json()
    return response
