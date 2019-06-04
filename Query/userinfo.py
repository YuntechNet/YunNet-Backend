from pymysql import MySQLError
from Base.SQL import SQLBase
from sanic.log import logger


class User(SQLBase):
    def get_userinfo(self, username: str) -> tuple:
        """Get userinfo by username

        Args:
            username: username

        Returns:
            tuple

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

        """
        with self.connection.cursor() as cursor:
            sql: str = (
                "SELECT * FROM `userinfo` WHERE "
                "`account` = %username OR `bed_id` = %username"
            )
            para_input = {"username": username}
            cursor.execute(sql, para_input)
            return cursor.fetchone()

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
                   "`department` = %department, "
                   "`name` = %name, "
                   "`lock_date` = %lock_date, "
                   "`unlock_date` = %unlock_date, "
                   "`launch_time` = %launch_time, "
                   "`bed_id` = %bed_id, "
                   "`ip_id` = %ip_id, "
                   "`token` = %token, "
                   "`back_mail` = %back_mail, "
                   "`back_mac` = %back_mac, "
                   "`last_log` = %last_log "
                   "WHERE `account = %account`")
            para_input = {"account": userinfo[0],
                          "department": userinfo[1],
                          "name": userinfo[2],
                          "lock_date": userinfo[3],
                          "unlock_date": userinfo[4],
                          "launch_time": userinfo[5],
                          "bed_id": userinfo[6],
                          "ip_id": userinfo[7],
                          "token": userinfo[8],
                          "back_mail": userinfo[9],
                          "back_mac": userinfo[10],
                          "last_log": userinfo[11], }
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
