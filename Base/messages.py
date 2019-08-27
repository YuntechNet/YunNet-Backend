from sanic.response import json


def msg(msg):
    return {"message": msg}


# user register
REGISTER_SUCCESS = json(msg("REGISTER_SUCCESS"), 200)
REGISTER_FAIL = json(msg("REGISTER_FAIL"), 400)
ALREADY_REGISTERED = json(msg("ALREADY_REGISTERED"), 400)
# user login
RECAPTCHA_FAILED = json(msg("RECAPTCHA_FAILED"), status=400)
LOGIN_FAILED = json(msg("LOGIN_FAILED"), status=400)
# user activation
ACTIVATION_SUCCESS = json(msg("ACTIVATION_SUCCESS"))
ACTIVATION_FAILED = json(msg("ACTIVATION_FAILED"), status=401)
# user password
PASSWORD_DOES_NOT_MATCH = json(msg("PASSWORD_NOT_MATCH"), status=400)
PASSWORD_SUCCESSFULLY_CHANGED = json(msg("PASSWORD_NOT_MATCH"), status=202)
# Token verify
TOKEN_EXPIRED = json(msg("TOKEN_EXPIRED"), status=410)
INVALID_TOKEN = json(msg("INVALID_TOKEN"), status=400)

OPERATION_SUCCESS = json(msg("OPERATION_SUCCESS"), status=200)
INVALID_SESSION = json(msg("INVALID_SESSION"), status=401)
SESSION_EXPIRED = json(msg("SESSION_EXPIRED"), status=401)
NO_PERMISSION = json(msg("NO_PERMISSION"), status=401)
INVALID_ENDPOINT = json(msg("INVALID_ENDPOINT"), status=404)
METHOD_NOT_SUPPORTED = json(msg("METHOD_NOT_SUPPORTED"), status=405)
INTERNAL_SERVER_ERROR = json(msg("INTERNAL_SERVER_ERROR"), status=500)
SERVICE_UNAVAILABLE = json(msg("SERVICE_UNAVAILABLE"), status=503)
