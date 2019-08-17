from datetime import datetime
from pymysql import MySQLError
from sanic.log import logger
from Base import SQLPool
from Base.types import LockTypes


class Lock:
    @staticmethod
    async def get_lock(ip: str) -> list:
        """Get user lock status by username

        Args:
            ip: ip address

        Returns:
            list dict.

            List is formatted as this:
            [
                {
                    lock_id: int,
                    lock_type_id: int,
                    ip: str,
                    lock_date: datetime
                    unlock_date: datetime
                    description: str,
                    lock_by_user_id: int
                },
            ]

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "SELECT * FROM `lock` WHERE `ip` = %s ORDER BY `lock_date` DESC"
                para_input = ip
                await cur.execute(sql, para_input)
                data = await cur.fetchall()
                key = [
                    "lock_id",
                    "lock_type_id",
                    "ip",
                    "lock_date",
                    "unlock_date",
                    "description",
                    "lock_by_user_id",
                ]

                dicts = [dict(zip(key, d)) for d in data]

        return dicts

    @staticmethod
    async def set_lock(
        ip: str,
        lock_type: LockTypes,
        lock_date: datetime,
        unlock_date: datetime = None,
        description: str = None,
        lock_by_user_id=None,
    ) -> bool:
        """set user lock by username

        Args:
            ip: ip address, str
            lock_type: locktypes, int or LockTypes
            lock_date: lock date, datetime
            unlock_date:  unlock date, datetime
            description: description, str
            lock_by_user_id: lock by user, int

        Returns:
            bool. If lock data is success set return True,
            if catch error return False.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "INSERT INTO `lock` VALUES (null, %s, %s, %s, %s, %s, %s)"
                para_input = (
                    lock_type,
                    ip,
                    lock_type,
                    unlock_date,
                    description,
                    lock_by_user_id,
                )
                await cur.execute(sql, para_input)
                await conn.commit()
                return True
