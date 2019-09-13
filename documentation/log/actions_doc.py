from sanic_openapi import api, doc

from documentation.universal_model import Message


class ActionGetLogDoc(api.API):
    summary = "Get User's action log."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = Message

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
