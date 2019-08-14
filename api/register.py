from sanic.response import json
from sanic_openapi import doc

from Base import messages
from Query import User
from Query.bed import Bed

from .login import bp_login

# a.k.a. account activate
@bp_login.route("/register", methods=["POST"], strict_slashes=True,)
@doc.consumes(
    doc.JsonBody({"id": str, "bed": str}),
    content_type="application/json",
    location="body",
    required=True,
)
@doc.produces()
async def bp_register(request):
    id = request.json["id"]
    bed = request.json["bed"]
    user_bed = await Bed().get_user_bed_info(id)

    if user_bed is None:
        return messages.NO_PERMISSION

    if user_bed["bed"] == bed:
        if await User().set_group(id, 3):
            resp = json({"message": "register complete"}, 200)
        else:
            resp = json({"message": "register fail"}, 500)
    else:
        resp = json({"message": "wrong bed_id or id"}, 400)

    return resp
