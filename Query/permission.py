from pymysql import MySQLError
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from sanic.log import logger

from Base import SQLPool


class Permission:
    @staticmethod
    async def check_permission(username, pstr) -> bool:
        """Check if user have the required permission

        """

        sql = (
            "SELECT EXISTS "
            "(SELECT * FROM `user` AS u "
            "INNER JOIN `group_user` AS gu ON u.uid = gu.uid "
            "INNER JOIN `group` AS g on gu.gid = g.gid "
            "INNER JOIN `group_permission` AS gp ON gp.gid = g.gid "
            "INNER JOIN `permission` AS p ON p.pid = gp.pid "
            "WHERE u.username = %s "
            "AND p.str = %s )"
        )
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                para_input = (username, pstr)
                await cur.execute(sql, para_input)
                out = await cur.fetchall()
                if out[0][0] != 1:
                    return True
                else:
                    return False

    @staticmethod
    async def get_all_permission(username) -> tuple:
        sql = (
            "SELECT p.str FROM `user` AS u "
            "INNER JOIN `group_user` AS gu ON u.uid = gu.uid "
            "INNER JOIN `group` AS g on gu.gid = g.gid "
            "INNER JOIN `group_permission` AS gp ON gp.gid = g.gid "
            "INNER JOIN `permission` AS p ON p.pid = gp.pid "
            "WHERE u.username = %s"
        )
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, username)
                permission_list_list = await cur.fetchall()
                permission_list = []
                for p in permission_list_list:
                    permission_list.append(p[0])
                return permission_list

