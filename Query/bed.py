from pymysql import MySQLError
from sanic.log import logger

from Base import SQLPool


class Bed:
    async def get_user_bed_info(self, uid):
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
                    "SELECT b.`bed`,b.`portal` "
                    "FROM `bed` as b "
                    "INNER JOIN `user` as u ON b.`bed` = u.`bed` "
                    "WHERE u.`uid` = %s "
                )
                para_input = uid
                await cur.execute(sql, para_input)
                data = await cur.fetchone()

                key = ["bed", "portal"]
                dicts = dict(zip(data, key))

        return dicts
