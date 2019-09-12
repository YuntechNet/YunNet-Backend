from datetime import datetime
import time

from jwt import decode as jwt_decode
from motor.motor_asyncio import AsyncIOMotorClient
from sanic.request import Request



__all__ = ["MongoDB"]

class MongoDB:
    """
    MongoDB namespace
    """
    _initialized = False
    _client = {}
    @staticmethod
    async def init(mongo_uri):
        MongoDB._client = AsyncIOMotorClient(mongo_uri)
        MongoDB._initialized = True
    @staticmethod
    async def close():
        if MongoDB._initialized:
            del(MongoDB._client)

    @staticmethod
    def _generate_endoint_access_entry(request, response):
        real_ip = request.ip
        if "X-Forwarded-For" in request.headers:
            real_ip = request.headers["X-Forwarded-For"]

        real_ip: str = request.ip
        username: str = None
        # Request.ip
        if "X-Forwarded-For" in request.headers:
            real_ip = request.headers["X-Forwarded-For"]
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"].split()
            if auth[0] == "Bearer":
                try:
                    jwt_payload = jwt_decode(request.app.config.JWT["jwtSecret"])
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
        except:
            body = request.body.decode("utf-8")
        session = None
        if "Authorization" in request.headers:
            session = request.headers["Authorization"]
        timenow = datetime.datetime.now()
        log_entry = {
            "http_status": response.status,
            "timestamp": timenow,
            "unix_time": time.mktime(timenow.timetuple()),
            "method": request.method,
            "session": session,
            "ip": real_ip,
            "username": username,
            "endpoint": request.path,
            "query_string": request.query_string,
            "request_body": request.json,
            "response_body": response.json,
        }
        return log_entry
    @staticmethod
    async def log_endpoint_access(request, response):
        log_entry = MongoDB._generate_endoint_access_entry(request,response)
        # get collection
        yunnet_db = MongoDB._client["yunnet"]
        log_collection = yunnet_db["log"]
        await log_collection.insert_one(log_entry)
