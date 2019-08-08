from sanic import Blueprint

from .user import bp_user
from .password import bp_password
from .department import bp_department
from .bed import bp_bed
from .ip import bp_ip

user = Blueprint.group(bp_user,
                       bp_password,
                       bp_department,
                       bp_bed,
                       bp_ip,
                       url_prefix='/user/<username>')
