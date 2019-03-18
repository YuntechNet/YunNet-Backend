from sanic import Blueprint

from .change_password import change_password
from .info import info
from .login import login
from .mac import mac
from .netflow import netflow
from .register import register
from .reset_password import reset_password


user = Blueprint.group(change_password, 
                       info, 
                       login, 
                       mac, 
                       netflow, 
                       register, 
                       reset_password, 
                       url_prefix='/user')
