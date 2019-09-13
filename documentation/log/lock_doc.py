from sanic_openapi import api, doc

from documentation.universal_model import Message


class LockLog:
    type = doc.String("lock or unlock")
    ip = doc.String("Locked ip")
    current_ip_owner = doc.Integer("Locked user's id")
    operator = doc.Integer("User's id who issues lock")
    lock_until = doc.String("lock or unlock date YYYY-mm-DD HH:MM:SS")
    id = doc.String("MongoDb id")

class LockGetLogByUsernameDoc(api.API):
    summary = "Get user's lock log by username."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = doc.List(LockLog)

    class FailResp:
        code = 500
        description = "On failed request"

        model =  Message

    response = [SuccessResp, FailResp]


class LockGetLogByIpDoc(api.API):
    summary = "Get user's lock log by ip."

    class SuccessResp:
        code = 200
        description = "On success request"

        model = doc.List(LockLog)

    class FailResp:
        code = 500
        description = "On failed request"

        model = Message

    response = [SuccessResp, FailResp]
