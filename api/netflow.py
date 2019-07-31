from sanic.response import json
from sanic import Blueprint

bp_netflow = Blueprint('netflow')


# TODO(biboy1999): filter for paging or datetime
@bp_netflow.route('/netflow/<ip>', methods=['GET'])
async def bp_netflow_offset(request, ip):
    netflow_data = {
        'netflow': [
            {
                'date': '2020-1-2',
                'lan_download': 500,
                'lan_upload': 600,
                'wan_download': 32767,
                'wan_upload': 1024
            },
            {
                'date': '2020-1-1',
                'lan_download': 7,
                'lan_upload': 87,
                'wan_download': 6,
                'wan_upload': 3
            },
        ]}
    response = json(netflow_data)
    return response

# @netflow.route('/netflow/<offset>', methods=['GET'])
# async def bp_netflow(request, offset):
#     response = json()
#     return response
