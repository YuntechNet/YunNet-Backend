from sanic.response import json
from sanic import Blueprint

bp = Blueprint('management-user-permission')

@bp.route('/permission/<ID>', methods=['POST'])
async def bp_permission(request):
    
    response =  json({})
    return response
