from sanic_openapi import api, doc

from documentation.universal_model import Message


class VerifyMailDoc(api.API):
    class SuccessResp:
        code = 200
        description = "On success request"

        model = Message

    class FailResp:
        code = 401
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
