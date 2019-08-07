from pymysql import MySQLError
from Base import SQLPool
from sanic.log import logger


class Userinfo:
    async def get_userinfo(self, user_id: int):
        """Get userinfo by username

        Args:
            username: username

        Returns:
            dict

            dict is formatted as this:
            (
                uid: int,
                username: string,
                password_hash: string,
                nick: string,
                bed: string,
                department: string,
                back_mail: string
            )

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql: str = ("SELECT * FROM `user` WHERE " "`uid` = %s")
                para_input = user_id
                await cur.execute(sql, para_input)
                data = await cur.fetchone()

                if data is None:
                    return None

                key = [
                    "uid",
                    "username",
                    "password_hash",
                    "nick",
                    "bed",
                    "department",
                    "back_mail",
                ]

                dicts = dict(zip(key, data))
        return dicts

    # TODO(biboy1999): WIP management logic
    # def set_userinfo(self, userinfo: tuple) -> bool:
    #     """Set userinfo with tuple
    #
    #     Args:
    #         userinfo:tuple
    #             Tuple is formatted as this:
    #             (
    #                 account: str, # can't be null
    #                 department: str, #cant be null
    #                 name: str,
    #                 lock_date: datetime,
    #                 unlock_date: datetime,
    #                 launch_time: datetime,
    #                 bed_id: string,
    #                 ip_id: string,
    #                 token: string,
    #                 back_email: string,
    #                 back_mac: string,
    #                 last_log: datetime
    #             )
    #
    #     Returns:
    #         bool. If set is success return True,
    #         if catch error return False.
    #
    #     """
    #     with self.connection.cursor() as cursor:
    #         sql = ("UPDATE userinfo SET "
    #                "`department` = %s, "
    #                "`name` = %s, "
    #                "`lock_date` = %s, "
    #                "`unlock_date` = %s, "
    #                "`launch_time` = %s, "
    #                "`bed_id` = %s, "
    #                "`ip_id` = %s, "
    #                "`token` = %s, "
    #                "`back_mail` = %s, "
    #                "`back_mac` = %s, "
    #                "`last_log` = %s "
    #                "WHERE `account = %s`")
    #         para_input = (userinfo[1], userinfo[2], userinfo[3], userinfo[4],
    #                       userinfo[5], userinfo[6], userinfo[7], userinfo[8],
    #                       userinfo[9], userinfo[10], userinfo[11], userinfo[0])
    #         try:
    #             cursor.execute(sql, para_input)
    #             self.commit()
    #             return True
    #         except MySQLError as e:
    #             self.rollback()
    #             logger.error("got error {}, {}".format(e, e.args[0]))
    #             logger.error("fail to udpate `userinfo` table SQL:{}".format(
    #                 cursor.mogrify(sql, para_input)))
    #             return False
