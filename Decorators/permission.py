from functools import wraps
from sanic.log import logger
from sanic.response import json
import jwt
from Base import messages
from Query import Permission


def permission(s):
    """check user permission

    must be warp before all decorator

    Args:
        s: permission string
    """

    def decorator(f):
        @wraps(f)
        async def permission_decorator(request, *args, **kwargs):
            if "permission" not in request:
                return messages.INVALID_SESSION
            elif not s in request["permission"]:
                return messages.NO_PERMISSION
            return await f(request, *args, **kwargs)
        return permission_decorator
    return decorator
