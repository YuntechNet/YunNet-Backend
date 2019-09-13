from sanic_openapi import api, doc

from documentation.universal_model import Message


class LockGetLogByUsernameDoc(api.API):
    summary = "Get user's lock log by username."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = Message

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]


class LockGetLogByIpDoc(api.API):
    summary = "Get user's lock log by ip."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = Message

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
