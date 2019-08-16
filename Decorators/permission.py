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
                return messages.INVALID_SESSION

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
                return messages.SESSION_EXPIRED
            except jwt.PyJWTError as ex:
                logger.warning(ex)
                return messages.INVALID_SESSION

            username = payload["username"]
            is_authorized = await Permission.check_permission(username, code)

            if is_authorized:
                request.args["token_username"] = username
                response = await f(request, *args, **kwargs)
                return response
            else:
                return messages.NO_PERMISSION

        return permission_decorator

    return decorator
