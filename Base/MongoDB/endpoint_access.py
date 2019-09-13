from datetime import datetime
from time import mktime

from jwt import decode as jwt_decode

from Base import MongoDB

def _generate_endoint_access_entry(request, response, jwt_secret):
    real_ip: str = request.ip
    username: str = None
    # Request.ip
    if "X-Forwarded-For" in request.headers:
        real_ip = request.headers["X-Forwarded-For"]
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"].split()
        if auth[0] == "Bearer":
            try:
                jwt_payload = jwt_decode(auth[1], jwt_secret)
                username = jwt_payload["username"]
            except:
                pass
    
    body = None
    try:
        body = request.json
        if body is not None:
            keys = "password", "old_password", "new_password"
            for key in keys:
                if key in body:
                    body.pop(key)
    except:request.body.decode("utf-8")
    session = None
    if "Authorization" in request.headers:
        session = request.headers["Authorization"]
    timenow = datetime.now()
    log_entry = {
        "http_status": response.status,
        "timestamp": timenow,
        "unix_time": mktime(timenow.timetuple()),
        "method": request.method,
        "session": session,
        "ip": real_ip,
        "username": username,
        "endpoint": request.path,
        "query_string": request.query_string,
        "request_body": body,
        "response_body": response.body,
    }
    return log_entry

async def log_endpoint_access(request, response, jwt_secret):
    log_entry = _generate_endoint_access_entry(request,response, jwt_secret)
    yunnet_db = MongoDB._client["yunnet"]
    log_collection = yunnet_db["log"]
    await log_collection.insert_one(log_entry)

