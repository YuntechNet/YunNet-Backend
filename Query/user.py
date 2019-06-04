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
                   "VALUES (%username, %department, %name)")
            para_input = {"username": username, "department": "",
                          "name": name}
            sql_user = (
                "INSERT INTO `user` (`account_id`, `passwd`, `group_id`, "
                "`exclude_per`, `extend_per`, `extend_group`) "
                "VALUES (%username, %password, %group,"
                " %exc_per, %ext_per, %ext_group)")
            para_input2 = {"username": username,
                           "password": password,
                           "group": group_code,
                           "exc_per": "[]",
                           "ext_per": "[]",
                           "ext_group": "[]"}
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

        Returns:
            tuple:
            (
                username -- string of username
            )
        """
        sql = ("SELECT `account` "
               "FROM `userinfo` "
               "WHERE  %query IN (`account`, `bed_id`, `ip_id`)")
        para_input = {'query': self.connection.escape_string(query)}
        with self.connection.cursor() as cur:
            cur.execute(sql, para_input)
            return cur.fetchone()

    def get_password(self, username: str) -> str:
        """Get user's password hash

        Args:
            username: username

        Returns:
            str. User's password hash

        """
        with self.connection.cursor() as cur:
            sql = ("SELECT `passwd` "
                   "FROM `user` "
                   "WHERE `account_id` = %username")
            para_input = {"username": username}
            cur.execute(sql, para_input)
        return cur.fetchone()

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
                   "SET `passwd` = %password "
                   "WHERE `account_id` = %username")
            para_input = {"username": username,
                          "password": password}
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
