from sanic.blueprints import Blueprint

from .user import user
from .log import bp_log
from .announcement import announcement
from .ip import bp_ip

management = Blueprint.group(user, bp_log, announcement, bp_ip, url_prefix='/management')
