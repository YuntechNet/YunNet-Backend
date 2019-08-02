from pymysql import MySQLError
from sanic.log import logger
from Base import SQLPool


class Lock():
    async def get_lock(self, username: str) -> list:
        """Get user lock status by username

        Args:
            username:username

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
                sql = ("SELECT `dorm_lock`.`id`,`dorm_lock`.`lock_date`,"
                    "`dorm_lock`.`unlock_date`,`dorm_lock`.`reason`,"
                    "`dorm_lock`.`description`,`dorm_lock`.`ip_id` "
                    "FROM `userinfo`"
                    "INNER JOIN `ip` ON `userinfo`.`ip_id` = `ip`.`ip`"
                    "INNER JOIN `dorm_lock` ON `dorm_lock`.`ip_id` = `ip`.`ip`"
                    "WHERE `userinfo`.`account` = %s")
                para_input = (username)
                await cur.execute(sql, para_input)
                data = cur.fetchall()
                key = ['id', 'lock_date', 'unlock_date', 'reason',
                    'description', 'ip_id']

                dicts = [dict(zip(key, d)) for d in data]

        return dicts

    async def set_lock(self, username: str, lock_date: str, unlock_date: str,
                 reason: str, description: str) -> bool:
        """set user lock by username

        Args:
            username: username
            lock_date: lock date with str format YYYY-MM-DD
            unlock_date:  unlock date with str format YYYY-MM-DD
            reason: reason
            description: description

        Returns:
            bool. If lock data is success set return True,
            if catch error return False.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = ("INSERT INTO `dorm_lock` "
                    "(`lock_date`,`unlock_date`,`reason`,`description`,`ip_id`)"
                    "SELECT %s,%s,%s,%s, ui.`ip_id` "
                    "FROM `userinfo` as ui "
                    "WHERE ui.`account` = %s")
                para_input = (
                    username, lock_date, unlock_date, reason, description)
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    await conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error("fail to insert `dorm_lock` table SQL:{}".format(
                        await cur.mogrify(sql, para_input)))
                    return False
