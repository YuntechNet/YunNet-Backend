from sanic.blueprints import Blueprint

from .user import bp_user
from .log import bp_log
from .abuse import abuse
from .announcement import announcement
from .ip import bp_ip
from .bulk_import import bp_bulk_import
from .netflow import netflow


management = Blueprint.group(
    bp_user, bp_log, announcement, bp_ip, bp_bulk_import, abuse, netflow, url_prefix="/management"
)
