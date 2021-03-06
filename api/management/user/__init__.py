from sanic import Blueprint

from .query import bp_query
from .manage import bp_user_manage
from .lock import bp_lock

bp_user = Blueprint.group(bp_query, bp_user_manage, bp_lock, url_prefix="/user")
