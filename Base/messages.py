from sanic.response import json


def msg(msg):
    return {"message": msg}


# user login
RECAPTCHA_FAILED = json(msg("RECAPTCHA_FAILED"), status=401)
LOGIN_FAILED = json(msg("LOGIN_FAILED"), status=401)
# user activation
ACTIVATION_SUCCESS = json(msg("ACTIVATION_SUCCESS"))
ACTIVATION_FAILED = json(msg("ACTIVATION_FAILED"), status=401)
INVALID_SESSION = json(msg("INVALID_SESSION"), status=401)
SESSION_EXPIRED = json(msg("SESSION_EXPIRED"), status=401)
NO_PERMISSION = json(msg("NO_PERMISSION"), status=403)
INVALID_ENDPOINT = json(msg("INVALID_ENDPOINT"), status=404)
METHOD_NOT_SUPPORTED = json(msg("METHOD_NOT_SUPPORTED"), status=405)
INTERNAL_SERVER_ERROR = json(msg("INTERNAL_SERVER_ERROR"), status=500)
