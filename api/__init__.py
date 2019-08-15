from sanic.blueprints import Blueprint

from .user import user
from .management import management
from .announcement import bp_announcement
from .login import bp_login
from .netflow import bp_netflow
from .register import bp_login
from .teapot import bp_teapot

api = Blueprint.group(
    user,
    management,
    bp_announcement,
    bp_login,
    bp_netflow,
    bp_teapot,
    url_prefix="/api",
)
