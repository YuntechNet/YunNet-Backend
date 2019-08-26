from aiomysql import DictCursor
from sanic.log import logger

from Base import SQLPool


class Group:
    @staticmethod
    async def get_user_group(username):
        """

        Args:
            username: username
        Returns:

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = (
                    "SELECT g.gid, g.name, g.description "
                    "FROM `user` AS u "
                    "INNER JOIN `group_user` AS gu ON u.uid = gu.uid "
                    "INNER JOIN `group` as g ON g.gid = gu.gid "
                    "WHERE u.username = %s "
                )
                para_input = username
                await cur.execute(sql, para_input)
                data = await cur.fetchall()

                if data is None:
                    return None

        return data

    # TODO(biboy1999): group str instead of gid?
    @staticmethod
    async def add_user_group(username, gid):
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "INSERT INTO `group_user` "
                    "SELECT %s, u.uid "
                    "FROM `user` AS u "
                    "WHERE u.username = %s "
                )
                para_input = (gid, username)
                affect_row = await cur.execute(sql, para_input)

                if affect_row:
                    return True
                else:
                    return False

    @staticmethod
    async def remove_user_group(username, gid):
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "DELETE gu "
                    "FROM `group_user` AS gu "
                    "INNER JOIN `user` AS u ON gu.uid = u.uid "
                    "WHERE u.username = %s "
                    "AND gu.gid = %s "
                )
                para_input = (username, gid)
                affect_row = await cur.execute(sql, para_input)

                if affect_row:
                    return True
                else:
                    return False
