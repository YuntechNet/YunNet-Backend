import jwt
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc

import config
from Base.jwt_payload import jwt_payload
from Query.user import User
from Query.permission import Permission

login = Blueprint('login')


@login.route('/login', methods=['POST'])
@doc.consumes(doc.JsonBody({'username': str, 'password': str}),
              content_type='application/json', location='body')
async def bp_login(request):
    try:
        username = request.json['username']
        password = request.json['password']

        # check login permission
        allowed = Permission().check_permission(username, '4701')

        if not allowed:
            return json({'message': 'no permission'}, 403)

        db_pw = User().get_password(username)

        if db_pw != password:
            return json({'message': 'Username/Password combination incorrect'},
                        401)
        token = jwt.encode(jwt_payload(username), config.JWT['jwtSecret'],
                           config.JWT['algorithm'])

        resp = json({'username': username, 'token': token}, 200)

    except KeyError as e:
        return json({'message': 'Username/Password combination incorrect'},
                    401)
    return resp
