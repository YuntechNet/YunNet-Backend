from asyncio import create_task
from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc, api

from Base import messages
from BackgroundJobs import bulk_import, BulkImportStatus
from Decorators import permission
import config as config_def

user_import = Blueprint("management-user-import")


@doc.consumes(doc.File, location="formData", required=True)
@user_import.route("/import", methods=["POST"], strict_slashes=True)
@permission("api.bed.import")
async def bp_bulk_import_file_upload(request):
    csv = request.files["file"][0].body
    create_task(bulk_import(csv, request.app.config.PASSWORD_SALT))
    return messages.ACCEPTED


@user_import.route("/import/status", methods=["GET"], strict_slashes=True)
async def bp_bulk_import_status(request):
    if BulkImportStatus.lock.locked():
        return json({"message": BulkImportStatus.message}, 202)
    else:
        return messages.OPERATION_SUCCESS


