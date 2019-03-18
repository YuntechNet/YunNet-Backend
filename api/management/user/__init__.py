from sanic import Blueprint

from .info import info
from .manage import manage
from .netflow import netflow

user = Blueprint.group(info, manage, netflow, url_prefix='/user')
