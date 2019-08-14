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
            async with conn.cursor() as cur:
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

                key = ["gid", "name", "description"]
                dicts = [dict(zip(key, d)) for d in data]

        return dicts
