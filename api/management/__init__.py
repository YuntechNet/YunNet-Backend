from sanic.blueprints import Blueprint

from .user import user
from .log import log
from .announcement import announcement

management = Blueprint.group(user, log, announcement, url_prefix='/management')
