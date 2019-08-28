from Base import messages
from sanic.response import json
from sanic import Blueprint

abuse = Blueprint("management-abuse", url_prefix="/abuse")

@abuse.route("/")
def bp_abuse(request):
    return messages.INVALID_ENDPOINT
