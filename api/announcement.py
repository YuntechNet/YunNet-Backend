from pymysql import MySQLError
from sanic.log import logger
from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc, api

from Base import messages
from Decorators import permission
from Query.announcement import Announcement

bp_announcement = Blueprint("announcement")


class announcement_get_list_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            post_id = doc.String("Post id")
            title = doc.String("Title name")

        model = dict(vars(model))

    class FailResp:
        code = 500
        description = "On failed request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp]


@announcement_get_list_doc
@bp_announcement.route("/announcement", methods=["GET"])
async def bp_announcement_get_list(request):
    resp = await Announcement.get_announcement()
    return json(resp)


class announcement_get_post_doc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        class model:
            post_id = doc.String("Post id")
            title = doc.String("Title name")
            content = doc.String("Content, may contain html")

        model = dict(vars(model))

    class FailResp:
        code = 500
        description = "On failed request"

        class model:
            message = doc.String("Error message")

        model = dict(vars(model))

    response = [SuccessResp, FailResp]


@announcement_get_post_doc
@bp_announcement.route("/announcement/<post_id>", methods=["GET"])
async def bp_single_announcement(request, post_id):
    resp = await Announcement.get_announcement_post(post_id)
    return json(resp)
