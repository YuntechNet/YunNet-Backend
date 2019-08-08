from pymysql import MySQLError
from sanic.log import logger
from Base import SQLPool


class MAC:
    async def get_mac(self, username: str) -> tuple:
        """get mac by username

        Args:
            username:username

        Returns:
            dict

            dict is formatted as this:
            (
                mac: str
            )

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "SELECT ip.mac FROM userinfo "
                    "INNER JOIN ip ON userinfo.ip_id = ip.ip "
                    "WHERE userinfo.account = %s"
                )
                para_input = username
                await cur.execute(sql, para_input)

                data = await cur.fetchone()
        return data[0]

    async def set_mac(self, account: str, mac: str) -> bool:
        """Set mac by account_id

        Args:
            account: account_id
            mac:mac address

        Returns:
            bool, If set success return True, if catch error return False.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = (
                    "UPDATE ip "
                    "INNER JOIN userinfo ON userinfo.ip_id = ip.ip "
                    "SET ip.mac = %s "
                    "WHERE userinfo.account = %s "
                )
                para_input = (mac, account)
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    await conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error(
                        "fail to udpate `ip` table SQL:{}".format(
                            await cur.mogrify(sql, para_input)
                        )
                    )
                    return False
