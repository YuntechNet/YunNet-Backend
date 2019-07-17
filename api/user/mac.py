from pymysql import MySQLError
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint

from Decorators import permission
from Query.mac import MAC

mac = Blueprint('mac')


@mac.route('/mac', methods=['GET'])
@permission('4200')
async def bp_mac(request, *args, **kwargs):
    username = kwargs.get('username', None)

    try:
        mac_str = MAC().get_mac(username)
    except MySQLError as e:
        logger.error('Catch MySQLError:{}'.format(e.args[1]))
        return json('messages.INTERNAL_SERVER_ERROR', 500)

    return json({'mac': mac_str})
