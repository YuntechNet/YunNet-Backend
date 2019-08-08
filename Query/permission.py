from pymysql import MySQLError
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from sanic.log import logger

from Base import SQLPool


class Permission:
    async def check_permission(self, username, pstr) -> bool:
        """Check if user have the required permission

        """

        sql = ("SELECT EXISTS "
               "(SELECT * FROM `user` AS u "
               "INNER JOIN `group_user` AS gu ON u.uid = gu.uid "
               "INNER JOIN `group` AS g on gu.gid = g.gid "
               "INNER JOIN `group_permission` AS gp ON gp.gid = g.gid "
               "INNER JOIN `permission` AS p ON p.pid = gp.pid "
               "WHERE u.username = %s "
               "AND p.str = %s )")
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                para_input = (username, pstr)
                await cur.execute(sql, para_input)
                out = await cur.fetchall()
                if out[0]:
                    return True
                else:
                    return False
