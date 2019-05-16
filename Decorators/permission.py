from functools import wraps
from sanic.response import json

from Decorators import debug

def permission(permission_code):
    def decorator(f):
        @debug
        @wraps(f)
        async def permission_decorator(request, *args, **kwargs):

            is_authorized = True
            #todo permission checking

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({'status': 'no_permission'}, 403)
        return permission_decorator
    return decorator

