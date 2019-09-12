from sanic.response import json
from sanic import Blueprint

from Query.announcement import Announcement
from documentation.announcement_doc import (
    AnnouncementGetListDoc,
    AnnouncementGetPostDoc,
)

bp_announcement = Blueprint("announcement")


@AnnouncementGetListDoc
@bp_announcement.route("/announcement", methods=["GET"])
async def bp_announcement_get_list(request):
    resp = await Announcement.get_announcement()
    return json(resp)


@AnnouncementGetPostDoc
@bp_announcement.route("/announcement/<post_id>", methods=["GET"])
async def bp_single_announcement(request, post_id):
    resp = await Announcement.get_announcement_post(post_id)
    return json(resp)
