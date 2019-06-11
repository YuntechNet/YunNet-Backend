from sanic.blueprints import Blueprint

from .user import user
from .log import bp_log
from .announcement import announcement

management = Blueprint.group(user, bp_log, announcement, url_prefix='/management')
