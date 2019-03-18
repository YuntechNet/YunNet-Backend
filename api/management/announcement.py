from sanic.response import json
from sanic import Blueprint

announcement = Blueprint('management-announcement', url_prefix='/announcement')

@announcement.route('/add', methods=['POST'])
async def bp_add(request):
    
    response =  json({})
    return response

@announcement.route('/edit/<ID>', methods=['POST'])
async def bp_edit(request):
    
    response =  json({})
    return response

@announcement.route('/delete/<ID>', methods=['POST'])
async def bp_delete(request):
    
    response =  json({})
    return response
