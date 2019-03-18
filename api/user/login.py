from sanic.response import json
from sanic import Blueprint

login = Blueprint('login')

@login.route('/login', methods=['POST'])
async def bp_login(request):
    #if success
    response = json({'session_key': '00000000-0000-0000-00000000'})
    #else
    #response = json({'message':'Username/Password combination incorrect'},
    #                 status=401) 
    return response
