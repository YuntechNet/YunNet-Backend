from pymysql import MySQLError
from sanic.log import logger

from Base import SQLPool


class Bed:
    async def get_user_bed_info(self, username):
        """

        Args:
            uid: user_id

        Returns:
            dict
            {
                bed: string
                portal: string
                ip: string

            }

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "SELECT i.description, ip_type_id "
                    "FROM `user` AS u "
                    "INNER JOIN `ip` AS i ON i.uid = u.uid "
                    "WHERE u.username = %s "
                    "AND (i.ip_type_id = 0 OR i.ip_type_id = 1)"
                )
                para_input = username
                await cur.execute(sql, para_input)

                data = await cur.fetchone()

                if data is None:
                    return None

                bed = data[0].split(".")

                dicts = {"portal": bed[0], "bed": bed[1], "ip_type": data[1]}

        return dicts
