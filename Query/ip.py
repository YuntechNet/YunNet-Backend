import datetime
import re

from aiomysql import DictCursor
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
    async def set_ip_type(ip, type):
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "UPDATE `iptable` SET `ip_type_id` = %s WHERE `ip` = %s "
                para_input = (type, ip)
                await cur.execute(sql, para_input)
                await conn.commit()
                return True

    @staticmethod
    async def assign_user(ip, uid):
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "UPDATE `iptable` SET `uid` = %s WHERE `ip` = %s "
                para_input = (uid, ip)
                await cur.execute(sql, para_input)
                await conn.commit()

                return True

    @staticmethod
    async def get_ip_by_id(ip):
        """

        Args:
            id:ip address

        Returns:dict
            {
                "ip": str,
                "switch_id": int,
                "ip_type_id": int,
                "mac": str,
                "port": int,
                "port_type": str,
                "is_updated": bool,
                "uid": int,
                "gid": int,
                "description": str,
                "lock_id": int,
            }

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "SELECT * FROM `iptable` WHERE `ip` = %s "
                para_input = ip
                await cur.execute(sql, para_input)
                data = await cur.fetchone()

                if data is None:
                    return None

                return data

    @staticmethod
    async def get_ip_by_bed(bed):
        """

        Args:
            bed:username

        Returns:dict
            {
                "ip": str,
                "switch_id": int,
                "ip_type_id": int,
                "mac": str,
                "port": int,
                "port_type": str,
                "is_updated": bool,
                "uid": int,
                "gid": int,
                "description": str,
                "lock_id": int,
            }

        """
        bed_regex = "^[A-Za-z][0-9]{3,4}-[0-9]$"
        portal_regex = "^[A-Za-z][0-9]{3,4}$"
        building_regex = "^[A-Za-z]$"
        if re.search(bed_regex, bed) is not None:
            sql = "SELECT * FROM `iptable` WHERE `description` LIKE CONCAT('%%',%s)"
        elif re.search(portal_regex, bed) is not None:
            sql = "SELECT * FROM `iptable` WHERE `description` LIKE CONCAT(%s,'%%')"
        elif re.search(building_regex, bed) is not None:
            sql = "SELECT * FROM `iptable` WHERE `description` LIKE CONCAT(%s,'%%')"
        else:
            return None

        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                para_input = bed
                await cur.execute(sql, para_input)
                data = await cur.fetchall()

                if data is None:
                    return None

                return data

    @staticmethod
    async def get_user_own_ip(username):
        """

        Args:
            username:username

        Returns:list with dict
            {
                "ip": str,
                "switch_id": int,
                "ip_type_id": int,
                "mac": str,
                "port": int,
                "port_type": str,
                "is_updated": bool,
                "uid": int,
                "gid": int,
                "description": str,
                "lock_id": int,
            }

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = (
                    "SELECT i.* "
                    "FROM `iptable` AS i "
                    "INNER JOIN `user` AS u ON u.`uid`= i.`uid` "
                    "WHERE u.`username` = %s "
                )
                para_input = username
                await cur.execute(sql, para_input)
                data = await cur.fetchall()

                if data is None:
                    return None

                return data
