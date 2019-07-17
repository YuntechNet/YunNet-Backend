from pymysql import MySQLError
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc

from Query.userinfo import Userinfo
from Query.user import User

register = Blueprint('register')


# a.k.a. account activate
@register.route('/register', methods=['POST'])
@doc.consumes(doc.JsonBody({'id': str, 'bed': str}),
              content_type='application/json',
              location='body',
              required=True)
async def bp_register(request):
    # 0200 -> 0300
    try:
        id = request.json['id']
        bed = request.json['bed']
        userinfo = Userinfo().get_userinfo(id)
    except KeyError:
        return json({'message': 'bad request'}, 400)
    except MySQLError as e:
        logger.error('Catch MySQLError:{}'.format(e.args[1]))
        return json('messages.INTERNAL_SERVER_ERROR', 500)

    if userinfo is None:
        return json({'message': 'id not found'}, 400)

    if userinfo['bed_id'] == bed:
        if User.set_group(id, '0300'):
            resp = json({'message': 'register complete'}, 200)
        else:
            resp = json({'message': 'register fail'}, 500)
    else:
        resp = json({'message': 'wrong bed_id or id'}, 400)

    return resp
