from functools import wraps
from sanic.log import logger
from sanic.response import json
import jwt
from Base import messages
from Query import Permission


def permission(code):
    """check user permission

    must be warp before all decorator

    Args:
        code: permission code
    """

    def decorator(f):
        # @debug
        @wraps(f)
        async def permission_decorator(request, *args, **kwargs):

            config = request.app.config

            if "Authorization" not in request.headers:
                return json(messages.INVALID_SESSION, 403)

            auth_header = request.headers["Authorization"]

            bearer = auth_header.split(" ", 1)
            token = bearer[1]

            payload = None
            try:
                payload = jwt.decode(
                    token, config.JWT["jwtSecret"], algorithms=config.JWT["algorithm"]
                )
            except jwt.ExpiredSignatureError as ex:
                logger.info(ex)
                return json(messages.SESSION_EXPIRED, 401)
            except jwt.PyJWTError as ex:
                logger.warning(ex)
                return json(messages.INVALID_SESSION, 401)

            query = Permission()

            username = payload["username"]

            is_authorized = query.check_permission(username, code)

            if is_authorized:

                response = await f(request, username=username, *args, **kwargs)
                return response
            else:
                return json(messages.NO_PERMISSION, 403)

        return permission_decorator

    return decorator
