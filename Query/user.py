from aiomysql import DictCursor
from pymysql import MySQLError
from sanic.log import logger
from Base import SQLPool


class User:
    @staticmethod
    async def delete_user(username):
        """Add user. Actually is Disable user

        Args:
            username: username.
        Returns:
            int. return affected row count.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = (
                    "DELETE gu "
                    "FROM `group_user` AS gu "
                    "INNER JOIN `user` AS u ON u.uid = gu.uid "
                    "WHERE u.username = %s"
                )
                para_input = username
                affected = await cur.execute(sql, para_input)
                # release user's used ip
                sql = (
                    "UPDATE `iptable` AS i "
                    "INNER JOIN `user` AS u "
                    "ON i.`uid` = u.`uid` "
                    "SET i.`uid` = 0 "
                    "WHERE u.`username` = %s "
                )
                affected = await cur.execute(sql, para_input)
                await conn.commit()
        return affected

    @staticmethod
    async def add_user(username, nick, department="", back_mail="", note=""):
        """Add new user.

        Args:
            username: username. str
            nick: user's name. str
            department: user's department. str
            back_mail: user's email. str
            note: note. str
        Returns:
            int. return affected row count.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "INSERT INTO `user` VALUES (null, %s, null, %s, %s, %s, %s)"
                para_input = (username, nick, department, back_mail, note)
                affected = await cur.execute(sql, para_input)
                await conn.commit()
        return affected

    @staticmethod
    async def get_user_id(username: str):
        """Get actual uid by username

        Args:
            username
        Returns:int, user id, if not found return None.
        """
        sql = "SELECT uid FROM `user` WHERE `username` = %s "
        para_input = username
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(sql, para_input)
                data = await cur.fetchone()
                await conn.commit()
                if len(data) == 0:
                    return None

        return data["uid"]

    @staticmethod
    async def get_username(uid: int):
        """Get actual username by uid

        Args:
            uid
        Returns:str, username, if not found return None.
        """
        sql = "SELECT username FROM `user` WHERE `uid` = %s "
        para_input = uid
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(sql, para_input)
                data = await cur.fetchone()
                await conn.commit()
                if len(data) == 0:
                    return None

        return data["username"]

    @staticmethod
    async def get_password(username: str) -> str:
        """Get user's password hash

        Args:
            username: username

        Returns:
            str. User's password hash,if user not found return empty string

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "SELECT `password_hash` FROM `user` WHERE `username` = %s"
                para_input = username
                await cur.execute(sql, para_input)
                data = await cur.fetchone()
                if data is None or len(data) == 0:
                    return ""
        return data["password_hash"]

    @staticmethod
    async def set_password(username: str, password: str) -> bool:
        """Set user password

        Args:
            username:username.
            password:password hash.

        Returns:
            bool. If set success return True, if catch error return False.

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "UPDATE `user` SET `password_hash` = %s WHERE `username` = %s"
                para_input = (password, username)
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    await conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error(
                        "fail to set user SQL:{}".format(
                            await cur.mogrify(sql, para_input)
                        )
                    )
                    return False
