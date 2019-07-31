from sanic.response import json
from sanic import Blueprint

bp_password = Blueprint('password')


@bp_password.route('/password', methods=['PATCH'])
async def bp_user_info(request, uid):
    response = json()
    return response
