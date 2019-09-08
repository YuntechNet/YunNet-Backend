from sanic.response import json


def msg(msg):
    return {"message": msg}


# user register
REGISTER_SUCCESS = json(msg("REGISTER_SUCCESS"), 200)
REGISTER_FAILED = json(msg("REGISTER_FAILED"), 400)
NOT_REGISTERED = json(msg("NOT_REGISTERED"), 400)
ALREADY_REGISTERED = json(msg("ALREADY_REGISTERED"), 400)
# user login
RECAPTCHA_FAILED = json(msg("RECAPTCHA_FAILED"), status=401)
LOGIN_FAILED = json(msg("LOGIN_FAILED"), status=401)
# user activation
ACTIVATION_SUCCESS = json(msg("ACTIVATION_SUCCESS"))
ACTIVATION_FAILED = json(msg("ACTIVATION_FAILED"), status=401)
# user password
PASSWORD_DOES_NOT_MATCH = json(msg("PASSWORD_NOT_MATCH"), status=400)
PASSWORD_SUCCESSFULLY_CHANGED = json(msg("PASSWORD_SUCCESSFULLY_CHANGED"), status=202)
# Token verify
TOKEN_EXPIRED = json(msg("TOKEN_EXPIRED"), status=410)
INVALID_TOKEN = json(msg("INVALID_TOKEN"), status=401)
# SMTP error
MAIL_REFUSED = json(msg("MAIL_REFUSED"), status=500)
# MAC
INVALID_MAC = json(msg("INVALID_MAC"), status=400)

# management
USER_ALREADY_EXISTS = json(msg("USER_ALREADY_EXISTS"), status=400)
USER_DOES_NOT_EXIST = json(msg("USER_DOES_NOT_EXIST"), status=404)

ACCEPTED = json(msg("ACCEPTED"), status=202)
OPERATION_SUCCESS = json(msg("OPERATION_SUCCESS"), status=200)
BAD_REQUEST = json(msg("BAD_REQUEST"), status=400)
INVALID_SESSION = json(msg("INVALID_SESSION"), status=401)
SESSION_EXPIRED = json(msg("SESSION_EXPIRED"), status=401)
NO_PERMISSION = json(msg("NO_PERMISSION"), status=401)
INVALID_ENDPOINT = json(msg("INVALID_ENDPOINT"), status=404)
METHOD_NOT_SUPPORTED = json(msg("METHOD_NOT_SUPPORTED"), status=405)
INTERNAL_SERVER_ERROR = json(msg("INTERNAL_SERVER_ERROR"), status=500)
SERVICE_UNAVAILABLE = json(msg("SERVICE_UNAVAILABLE"), status=503)
