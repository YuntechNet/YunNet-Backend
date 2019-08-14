import api
from sanic.response import text
from sanic import Blueprint
from sanic_openapi import doc

bp_teapot = Blueprint("teapot")


@bp_teapot.route("/teapot", methods=["GET"], strict_slashes=True)
async def teapot(request):
    import importlib.resources as pkg_resources

    teapot = pkg_resources.read_text(api, "teapot.txt")
    return text(teapot, status=418)
