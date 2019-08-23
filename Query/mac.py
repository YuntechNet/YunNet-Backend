from pymysql import MySQLError
from sanic.log import logger
from Base import SQLPool


class MAC:
    # @staticmethod
    # async def get_mac(username: str) -> tuple:
    #     """get mac by username
    #
    #     Args:
    #         username:username
    #
    #     Returns:
    #         dict
    #
    #         dict is formatted as this:
    #         (
    #             mac: str
    #         )
    #
    #     """
    #     async with SQLPool.acquire() as conn:
    #         async with conn.cursor() as cur:
    #             sql = (
    #                 "SELECT ip.mac FROM userinfo "
    #                 "INNER JOIN ip ON userinfo.ip_id = ip.ip "
    #                 "WHERE userinfo.account = %s"
    #             )
    #             para_input = username
    #             await cur.execute(sql, para_input)
    #
    #             data = await cur.fetchone()
    #     return data[0]

    @staticmethod
    async def set_mac(ip: str, mac: str) -> bool:
        """Set mac by account_id

        Args:
            ip: ip
            mac:mac address

        Returns:
            bool, If set success return True, if catch error return False.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "UPDATE `iptable` SET `mac` = %s WHERE `ip` = %s "
                para_input = (mac, ip)
                await cur.execute(sql, para_input)
                await conn.commit()
                return True
