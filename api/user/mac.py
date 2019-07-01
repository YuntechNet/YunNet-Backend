from sanic.response import json
from sanic import Blueprint

from Decorators import permission
from Query.mac import MAC

mac = Blueprint('mac')


@mac.route('/mac', methods=['GET'])
@permission('4200')
async def bp_mac(request, *args, **kwargs):
    username = kwargs.get('username', None)
    mac_str = MAC().get_mac(username)
    return json({'mac': mac_str})
