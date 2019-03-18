from sanic.response import json
from sanic import Blueprint

info = Blueprint('info')

@info.route('/info', methods=['GET'])
async def bp_info(request):
    user_obj = {'user':         'B11078763',
                'department':   '四資工一A',
                'name':         '陳凱文',
                'ip':           '8.8.8.8',
                'mac':          'FF:FF:FF:FF',
                'portal':       'C871',
                'bed':          'C876-3',
                'bed_type':     '一般房',
                'status':       '已使用/已註冊'
               }
    response =  json(user_obj)
    return response
