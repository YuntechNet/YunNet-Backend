from sanic.response import json
from sanic.request import Request
from sanic import Blueprint
from sanic_openapi import doc

bp_ip = Blueprint('management-ip', url_prefix='/ip')


@doc.summary("Query IP managed by the switch")
@doc.consumes(
    doc.JsonBody(
        {
            "switch": str,
            "mode": int,
            "status": int
        }
    ), content_type="application/json", location="body"
    )
@doc.produces(
    [
        {
            "ip": str,
            "mac": str,
            "switch": str,
            "port": int,
            "port_type": int,
            "mode": int,
            "status": int
        }
    ]
    , content_type="application/json"
    )
@bp_ip.route('', methods=['GET'])
def ip_get(request: Request):
    return json({})

@doc.summary('Update IP mode and status')
@doc.consumes(
    doc.JsonBody(
        [
            {
                "ip": str,
                "mode": int,
                "status": int
            }
        ]
    ), content_type="application/json", location="body"
)
@bp_ip.route('', methods=['PATCH'])
def ip_post(request: Request):
    return json({})
