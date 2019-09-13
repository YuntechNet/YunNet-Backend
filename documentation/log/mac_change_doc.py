from sanic_openapi import api, doc

from documentation.universal_model import Message


class MacChangeLog:
    ip = doc.String("User's ip address")
    owner = doc.String("Username")
    old_mac = doc.String("User's previous MAC address")
    new_mac = doc.String("User's new MAC address")
    date = doc.String("User's set MAC date YYYY-mm-DD HH:MM:SS")
    id = doc.String("MongoDb id")


class MacChangeGetLogByUsernameDoc(api.API):
    summary = "Get user's MAC change log by username."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = doc.List(MacChangeLog)

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

        model = doc.List(MacChangeLog)

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
