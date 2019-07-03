from pymysql import MySQLError
from Base.SQL import SQLBase
from sanic.log import logger


class Userinfo(SQLBase):
    def get_userinfo(self, username: str):
        """Get userinfo by username

        Args:
            username: username

        Returns:
            dict

            dict is formatted as this:
            (
                account: str, # can't be null
                department: str, #cant be null
                name: str,
                lock_date: datetime,
                unlock_date: datetime,
                launch_time: datetime,
                bed_id: string,
                ip_id: string,
                token: string,
                back_email: string,
                back_mac: string,
                last_log: datetime
            )

        """
        with self.connection.cursor() as cursor:
            sql: str = (
                "SELECT * FROM `userinfo` WHERE "
                "`account` = %s OR `bed_id` = %s"
            )
            para_input = (username, username)
            cursor.execute(sql, para_input)
            data = cursor.fetchone()

            if data is None:
                return None

            key = ['account', 'department', 'name', 'lock_date', 'unlock_date',
                   'launch_time', 'bed_id', 'ip_id', 'token', 'back_email',
                   'back_mac', 'last_log']

            dicts = dict(zip(key, data))
        return dicts

    def set_userinfo(self, userinfo: tuple) -> bool:
        """Set userinfo with tuple

        Args:
            userinfo:tuple
                Tuple is formatted as this:
                (
                    account: str, # can't be null
                    department: str, #cant be null
                    name: str,
                    lock_date: datetime,
                    unlock_date: datetime,
                    launch_time: datetime,
                    bed_id: string,
                    ip_id: string,
                    token: string,
                    back_email: string,
                    back_mac: string,
                    last_log: datetime
                )

        Returns:
            bool. If set is success return True,
            if catch error return False.

        """
        with self.connection.cursor() as cursor:
            sql = ("UPDATE userinfo SET "
                   "`department` = %s, "
                   "`name` = %s, "
                   "`lock_date` = %s, "
                   "`unlock_date` = %s, "
                   "`launch_time` = %s, "
                   "`bed_id` = %s, "
                   "`ip_id` = %s, "
                   "`token` = %s, "
                   "`back_mail` = %s, "
                   "`back_mac` = %s, "
                   "`last_log` = %s "
                   "WHERE `account = %s`")
            para_input = (userinfo[1], userinfo[2], userinfo[3], userinfo[4],
                          userinfo[5], userinfo[6], userinfo[7], userinfo[8],
                          userinfo[9], userinfo[10], userinfo[11], userinfo[0])
            try:
                cursor.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to udpate `userinfo` table SQL:{}".format(
                    cursor.mogrify(sql, para_input)))
                return False
