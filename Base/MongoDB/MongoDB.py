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

