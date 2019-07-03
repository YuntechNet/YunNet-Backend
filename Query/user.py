from pymysql import MySQLError
from sanic.log import logger
from Base.SQL import SQLBase


class User(SQLBase):
    def new_user(self, username: str, password: str, name: str,
                 group_code: str = '0100') -> bool:
        """Add new user.

        Args:
            username:username.
            password:password_hash.
            group_code:set user group, default is user.stop(0100).

        Returns:
            bool. If user successful added return True,
            if catch error return False.

        """
        with self.connection.cursor() as cur:
            sql = ("INSERT INTO `userinfo` (`account`, `department`, `name`) "
                   "VALUES (%s, %s, %s)")

            para_input = (username, "", name)
            sql_user = (
                "INSERT INTO `user` (`account_id`, `passwd`, `group_id`, "
                "`exclude_per`, `extend_per`, `extend_group`) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
            para_input2 = (username, password, group_code, "[]", "[]", "[]")
            try:
                cur.execute(sql, para_input)
                cur.execute(sql_user, para_input2)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to add userinfo SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                logger.error("fail to add user SQL:{}".format(
                    cur.mogrify(sql_user, para_input2)))
                return False

    def get_username(self, query: str) -> str:
        """Get actual username by username, bed, ip

        Args:
            query -- username, bed, or IP

        Returns:str, username, if not found return empty string.
        """
        sql = ("SELECT `account` "
               "FROM `userinfo` "
               "WHERE  %s IN (`account`, `bed_id`, `ip_id`)")
        para_input = (query)
        with self.connection.cursor() as cur:
            cur.execute(sql, para_input)
            data = cur.fetchone()

            if len(data) == 0:
                return ''
        return data[0]

    def get_password(self, username: str) -> str:
        """Get user's password hash

        Args:
            username: username

        Returns:
            str. User's password hash,if user not found return empty string

        """
        with self.connection.cursor() as cur:
            sql = ("SELECT `passwd` "
                   "FROM `user` "
                   "WHERE `account_id` = %s")
            para_input = (username)
            cur.execute(sql, para_input)
            data = cur.fetchone()
            if data is None or len(data) == 0:
                return ''
        return data[0]

    def set_password(self, username: str, password: str) -> bool:
        """Set user password

        Args:
            username:username.
            password:password hash.

        Returns:
            bool. If set success return True, if catch error return False.

        """
        with self.connection.cursor() as cur:
            sql = ("UPDATE `user` "
                   "SET `passwd` = %s "
                   "WHERE `account_id` = %s")
            para_input = (username, password)
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to set user SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False

    def set_group(self, username, group_id):
        with self.connection.cursor() as cur:
            sql = "UPDATE `user` SET `group_id` = %s WHERE `account_id` = %s"

            para_input = (group_id, username)
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to set user SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False
