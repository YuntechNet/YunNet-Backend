from functools import wraps
from sanic.response import json
from sanic.request import Request
from Base import messages

def debug(permission_code):
    def decorator(f):
        @wraps(f)
        async def debug_decorator(request: Request, *args, **kwargs):

            debug_mode = True
            is_developer = True
            # todo developer permission checking

            if not debug_mode or is_developer:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return messages.SERVICE_UNAVAILABLE
                
        return debug_decorator

    return decorator
