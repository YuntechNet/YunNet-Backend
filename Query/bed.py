from aiomysql import DictCursor
from pymysql import MySQLError
from sanic.log import logger, error_logger

from Base import SQLPool, messages


class Bed:
    @staticmethod
    async def get_user_bed_info(username):
        """

        Args:
            username: username

        Returns:
            dict
            {
                bed: string
                portal: string
                ip: string
            }

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = (
                    "SELECT i.description, ip_type_id "
                    "FROM `user` AS u "
                    "INNER JOIN `iptable` AS i ON i.uid = u.uid "
                    "WHERE u.username = %s "
                    "AND (i.ip_type_id = 0 OR i.ip_type_id = 1)"
                )
                para_input = username
                await cur.execute(sql, para_input)

                data = await cur.fetchone()

                if data is None:
                    return None

                if data["description"] == "":
                    error_logger.error(
                        "Dorm Ip found but description missing: {}".format(username)
                    )
                    return messages.INTERNAL_SERVER_ERROR

                bed = data["description"].split(".")

                dicts = {"portal": bed[0], "bed": bed[1], "ip_type": data["ip_type_id"]}

        return dicts
