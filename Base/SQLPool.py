import aiomysql


class SQLPool:
    """
    Create Pool object from parameters
    """

    pool: aiomysql.Pool = None

    @staticmethod
    async def acquire():
        return SQLPool.pool.acquire()

    @staticmethod
    async def init_pool(*args, **kwargs):
        if SQLPool.pool == None:
            SQLPool.pool = await aiomysql.create_pool(*args, **kwargs)
        return SQLPool
