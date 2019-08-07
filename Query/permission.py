from pymysql import MySQLError
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from sanic.log import logger

from Base import SQLPool


class Permission:
    async def check_permission(self, username, code) -> bool:
        """Check if user have the required permission

        """

        sql = ""
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                para_input = (username, username, code, code, code)
                await cur.execute(sql, para_input)
                out = await cur.fetchall()
                logger.debug(out)
                if len(out) <= 0:
                    return False
                else:
                    return True
