from sanic import Blueprint
from sanic_openapi import doc, api

from Base import messages

bp_bulk_import = Blueprint("bulk_import")


@doc.consumes(doc.File, location="formData", required=True)
@bp_bulk_import.route("/bulk-import", methods=["POST"], strict_slashes=True)
async def bulk_import_file_upload(request):
    return messages.OPERATION_SUCCESS
