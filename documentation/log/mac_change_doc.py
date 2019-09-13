from sanic_openapi import api, doc

from documentation.universal_model import Message


class MacChangeGetLogByUsernameDoc(api.API):
    summary = "Get user's MAC change log by username."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = Message

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]


class MacChangeGetLogByIpDoc(api.API):
    summary = "Get user's MAC change log by ip."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = Message

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
