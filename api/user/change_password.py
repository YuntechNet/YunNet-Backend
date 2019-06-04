from sanic.response import json
from sanic import Blueprint

change_password = Blueprint('change-password')


@change_password.route('/change-password', methods=['PUT'])
async def bp_change_password(request):
    # TODO: change password mechanism
    response = json({'message': 'SUCCESS'})
    return response
