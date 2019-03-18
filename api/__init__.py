from sanic.blueprints import Blueprint

from .user import user
from .announcement import announcement
from .management import management

api = Blueprint.group(user, announcement, management, url_prefix='/api')
