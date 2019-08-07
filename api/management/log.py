from sanic import Blueprint
from sanic.response import json

bp_log = Blueprint("management-log", url_prefix="/log")


@bp_log.route("", methods=["GET"])
def log_get(request):
    return json({})


@bp_log.route("", methods=["POST"])
def log_add(request):
    return json({})


@bp_log.route("/<log_id>", methods=["PUT"])
def log_edit(request, log_id):
    return json({})


@bp_log.route("/<log_id>", methods=["DELETE"])
def log_delete(request, log_id):
    return json({})
