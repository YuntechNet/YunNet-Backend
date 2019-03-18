from sanic.response import json
from sanic import Blueprint

manage = Blueprint('management-user-manage', url_prefix='/manage')

@manage.route('/permission/<ID>', methods=['POST'])
async def bp_permission(request):
    
    response =  json({})
    return response

@manage.route('/add/<ID>', methods=['POST'])
async def bp_add(request):
    
    response =  json({})
    return response

@manage.route('/delete/<ID>', methods=['GET', 'DELETE'])
async def bp_delete(request):
    
    response =  json({})
    return response
