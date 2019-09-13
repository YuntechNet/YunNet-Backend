from sanic import Blueprint

from .actions import bp_log_actions
from .lock import bp_log_lock
from .mac_change import bp_log_mac

bp_log = Blueprint.group(
    bp_log_actions, bp_log_lock, bp_log_mac, url_prefix="/log"
)
