from sanic import Blueprint

from .query import bp_query
from .manage import manage
from .netflow import netflow

bp_user = Blueprint.group(bp_query, manage, netflow, url_prefix="/user")
