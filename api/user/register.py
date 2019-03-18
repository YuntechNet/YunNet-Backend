from sanic.response import json
from sanic import Blueprint

register = Blueprint('register')

@register.route('/register', methods=['POST'])
async def bp_register(request):
    
    response =  json({})
    return response
