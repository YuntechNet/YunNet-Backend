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

    @staticmethod
    async def get_user_ip_mac(username):
        """

        Args:
            username:username

        Returns:dict
            {
                "ip":str,
                "mac":str
            }

        """
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

    @staticmethod
    async def get_user_own_ip(username):
        """

        Args:
            username:username

        Returns:list with dict
            {
                "ip": str,
                "switch_id": int,
                "status_id": int,
                "ip_type_id": int,
                "mac": str,
                "port": int,
                "port_type": str,
                "is_updated": bool,
                "uid": int,
                "gid": int,
                "description": str,
            }

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "SELECT i.* "
                    "FROM `ip` AS i "
                    "INNER JOIN `user` AS u ON u.`uid`= i.`uid` "
                    "WHERE u.`username` = %s "
                )
                para_input = username
                await cur.execute(sql, para_input)
                data = await cur.fetchall()

                if data is None:
                    return None

                key = [
                    "ip",
                    "switch_id",
                    "status_id",
                    "ip_type_id",
                    "mac",
                    "port",
                    "port_type",
                    "is_updated",
                    "uid",
                    "gid",
                    "description",
                ]
                dicts = [dict(zip(key, d)) for d in data]
                return dicts
