import aiomysql

class SQLPool:
    """
    Create Pool object from parameters
    """
    pool: aiomysql.Pool = None

    @staticmethod
    async def acquire():
        return SQLPool.pool.acquire()

    async def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        if SQLPool.pool == None:
            SQLPool.pool = await aiomysql.create_pool(*args, **kwargs)
        return self
