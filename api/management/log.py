from sanic import Blueprint
from sanic.response import json

log = Blueprint('management-log')

@log.route('/add', methods=['POST'])
def log_add(request):
    return json({})

@log.route('/edit', methods=['POST'])
def log_edit(request):
    return json({})

@log.route('/delete', methods=['POST'])
def log_delete(request):
    return json({})

