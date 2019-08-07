from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc

service = Blueprint("service")


@doc.summary("Query services")
@doc.produces(
    {"service": [{"ip": str, "description": str, "mac": str, "group": str}]},
    content_type="application/json",
)
@service.route("/service", methods="GET")
async def bp_service_get(request):
    response = json({})
    return response
