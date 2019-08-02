import asyncio
import aiomysql
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from config import SQL_CREDENTIALS

class SQLBase:
    """
    Create connection object from parameters
    """
    pool: aiomysql.Pool = None

    async def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        if SQLBase.pool == None:
            SQLBase.pool = await aiomysql.create_pool(*args, **kwargs)
        return self
