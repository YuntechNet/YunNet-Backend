from sanic import Blueprint

from .query import bp_query
from .manage import manage

bp_user = Blueprint.group(bp_query, manage, url_prefix="/user")
