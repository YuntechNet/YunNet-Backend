from pymysql import MySQLError
from sanic.log import logger

from Base import SQLPool


class log:
    async def get_log(self, offset=0):
        """get 100 log

        Args:
            offset:paging

        Returns:
            list dict.

            List is formatted as this:
            [
                {
                    id: int,
                    lock_date: datetime,
                    unlock_date: datetime,
                    reason: str,
                    description: str,
                    ip_id: str,
                },
            ]

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "SELECT * FROM `log` " "ORDER BY `datetime` DESC " "LIMIT %s,100"
                para_input = offset * 100
                await cur.execute(sql, para_input)
                data = await cur.fetchall()
                key = ["id", "datetime", "content", "account_id"]

                dicts = [dict(zip(key, d)) for d in data]

        return dicts

    async def delete_log(self, log_id):
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "DELETE FROM `log` WHERE `id` = 123"
                para_input = log_id
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error(
                        "fail to delete `log` table SQL:{}".format(
                            cur.mogrify(sql, para_input)
                        )
                    )
                    return False
