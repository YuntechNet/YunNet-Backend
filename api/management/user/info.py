from sanic.response import json
from sanic import Blueprint

info = Blueprint('management-user-info', url_prefix='/<user_id>')
