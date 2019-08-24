from sanic.blueprints import Blueprint

from .user import user
from .log import bp_log
from .announcement import announcement
from .ip import bp_ip
from .bulk_import import bp_bulk_import

management = Blueprint.group(
    user, bp_log, announcement, bp_ip, bp_bulk_import, url_prefix="/management"
)
