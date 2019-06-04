from sanic.response import json
from sanic import Blueprint

reset_password = Blueprint('reset-password')


@reset_password.route('/reset-password', methods=['POST'])
async def bp_reset_password(request):
    response = json({})
    return response
