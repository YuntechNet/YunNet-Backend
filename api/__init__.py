from sanic.blueprints import Blueprint

from .user import user
from .management import management
from .announcement import bp_announcement
from .token import bp_token
from .netflow import bp_netflow

api = Blueprint.group(
    user, management, bp_announcement, bp_token, bp_netflow, url_prefix="/api"
)
