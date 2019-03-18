from sanic.response import json
from sanic import Blueprint

mac = Blueprint('mac')

@mac.route('/mac', methods=['POST'])
async def bp_mac(request):
    
    response =  json({})
    return response
