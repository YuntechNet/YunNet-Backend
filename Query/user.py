from pymysql import MySQLError
from sanic.log import logger
from Base import SQLPool


class User():

    # TODO(biboy1999):WIP management logic
    # def new_user(self, username: str, password: str, name: str,
    #              group_code: str = '0100') -> bool:
    #     """Add new user.
    #
    #     Args:
    #         username:username.
    #         password:password_hash.
    #         group_code:set user group, default is user.stop(0100).
    #
    #     Returns:
    #         bool. If user successful added return True,
    #         if catch error return False.
    #
    #     """
    #     with self.connection.cursor() as cur:
    #         sql = ("INSERT INTO `userinfo` (`account`, `department`, `name`) "
    #                "VALUES (%s, %s, %s)")
    #
    #         para_input = (username, "", name)
    #         sql_user = (
    #             "INSERT INTO `user` (`account_id`, `passwd`, `group_id`, "
    #             "`exclude_per`, `extend_per`, `extend_group`) "
    #             "VALUES (%s, %s, %s, %s, %s, %s)")
    #         para_input2 = (username, password, group_code, "[]", "[]", "[]")
    #         try:
    #             cur.execute(sql, para_input)
    #             cur.execute(sql_user, para_input2)
    #             self.commit()
    #             return True
    #         except MySQLError as e:
    #             self.rollback()
    #             logger.error("got error {}, {}".format(e, e.args[0]))
    #             logger.error("fail to add userinfo SQL:{}".format(
    #                 cur.mogrify(sql, para_input)))
    #             logger.error("fail to add user SQL:{}".format(
    #                 cur.mogrify(sql_user, para_input2)))
    #             return False

    async def get_user_id(self, query: str) -> str:
        """Get actual username by username, bed, ip

        Args:
            query -- username, bed, or IP

        Returns:str, username, if not found return empty string.
        """
        sql = ("SELECT u.`uid` "
               "FROM `user` as u "
               "INNER JOIN `bed` as b ON u.`bed` = b.`bed` "
               "INNER JOIN `ip`  as i ON b.`ip` = i.`ip` "
               "WHERE %s IN (u.`username`, b.`bed`, i.`ip`)")
        para_input = query
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, para_input)
                data = await cur.fetchone()

                if len(data) == 0:
                    return ''

        return data[0]

    async def get_password(self, user_id: int) -> str:
        """Get user's password hash

        Args:
            user_id: user_id

        Returns:
            str. User's password hash,if user not found return empty string

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = ("SELECT `password_hash` "
                    "FROM `user` "
                    "WHERE `uid` = %s")
                para_input = user_id
                await cur.execute(sql, para_input)
                data = await cur.fetchone()
                if data is None or len(data) == 0:
                    return ''
        return data[0]

    async def set_password(self, username: str, password: str) -> bool:
        """Set user password

        Args:
            username:username.
            password:password hash.

        Returns:
            bool. If set success return True, if catch error return False.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = ("UPDATE `user` "
                    "SET `password_hash` = %s "
                    "WHERE `uid` = %s")
                para_input = (username, password)
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    await conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error("fail to set user SQL:{}".format(
                        await cur.mogrify(sql, para_input)))
                    return False

    # TODO(biboy1999):WIP management logic
    # def set_group(self, username, group_id):
    #     with self.connection.cursor() as cur:
    #         sql = "UPDATE `user` SET `group_id` = %s WHERE `account_id` = %s"
    #
    #         para_input = (group_id, username)
    #         try:
    #             cur.execute(sql, para_input)
    #             self.commit()
    #             return True
    #         except MySQLError as e:
    #             self.rollback()
    #             logger.error("got error {}, {}".format(e, e.args[0]))
    #             logger.error("fail to set user SQL:{}".format(
    #                 cur.mogrify(sql, para_input)))
    #             return False
