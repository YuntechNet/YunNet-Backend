import datetime

from pymysql import MySQLError
from sanic.log import logger

from Base import SQLPool


class Ip:
    # TODO(biboy1999): WIP management logic
    # def get_ip_by_switch(self, switch):
    #     with self.connection.cursor() as cur:
    #         sql = ("SELECT `ip`, `status`, `mac`, `update`, `port`"
    #                ", `ip`.`port_type`, `switch`.`location` "
    #                "FROM `ip` INNER JOIN `switch` "
    #                "ON `switch`.`id` = `ip`.`switch_id` "
    #                "WHERE `switch`.`location` = %s ")
    #         para_input = switch
    #         cur.execute(sql, switch)
    #         data = cur.fetchall()
    #         key = ['ip', 'status', 'mac', 'update', 'port', 'port_type',
    #                'switch']
    #
    #         dicts = [dict(zip(key, d)) for d in data]
    #
    #     return dicts

    async def get_user_ip_mac(self, username):
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "SELECT i.ip,i.mac "
                    "FROM `user` AS u "
                    "INNER JOIN `ip` AS i ON i.uid = u.uid "
                    "WHERE u.username = %s "
                )
                para_input = username
                await cur.execute(sql, para_input)
                data = await cur.fetchone()

                if data is None:
                    return None

                key = ["ip", "mac"]
                dicts = dict(zip(key, data))

        return dicts
