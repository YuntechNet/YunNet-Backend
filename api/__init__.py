from sanic.blueprints import Blueprint

from .user import user
from .management import management
from .announcement import bp_announcement
from .login import bp_login
from .netflow import bp_netflow
from .register import bp_login
from .teapot import bp_teapot
from .verify_mail import bp_verify_mail
from .forgot_password import bp_forgot_passowrd
from .log import bp_log

api = Blueprint.group(
    user,
    management,
    bp_announcement,
    bp_login,
    bp_netflow,
    bp_verify_mail,
    bp_teapot,
    bp_forgot_passowrd,
    bp_log,
    url_prefix="/api",
)
