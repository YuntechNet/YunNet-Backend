from sanic.response import json
from sanic import Blueprint

announcement = Blueprint('announcement')

@announcement.route('/announcement', methods=['GET'])
async def bp_add(request):
    
    response =  json({})
    return response

@announcement.route('/announcement/<ID>', methods=['GET'])
async def bp_add(request):
    
    response =  json({})
    return response
