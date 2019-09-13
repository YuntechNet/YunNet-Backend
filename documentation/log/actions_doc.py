from sanic_openapi import api, doc

from documentation.universal_model import Message


class Action:
    username = doc.String("Username")
    action = doc.String("User preformed action")
    id = doc.String("MongoDb id")
    date = doc.String("Action preformed time YYYY-mm-DD HH:MM:SS")


class ActionGetLogDoc(api.API):
    summary = "Get User's action log."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = doc.List(Action)

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
