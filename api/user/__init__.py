from sanic import Blueprint

from .user import bp_user
from .password import bp_password
from .ip import bp_ip
from .mac import bp_mac
from .lock import bp_lock

user = Blueprint.group(
    bp_user, bp_password, bp_ip, bp_mac, bp_lock, url_prefix="/user/<username>"
)
