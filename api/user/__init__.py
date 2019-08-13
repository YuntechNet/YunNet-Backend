from sanic import Blueprint

from .user import bp_user
from .password import bp_password
from .ip import bp_ip

user = Blueprint.group(bp_user, bp_password, bp_ip, url_prefix="/user/<username>")
