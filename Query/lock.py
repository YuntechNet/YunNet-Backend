from pymysql import MySQLError
from pymysql.connections import Connection
from sanic.log import logger

from Base.SQL import SQLBase


class Lock(SQLBase):
    def get_lock(self, username: str) -> list:
        """Get user lock status by username

        Args:
            username:username

        Returns:
            tuple list.

            Tuple is formatted as this:
            (
                id: int
                lock_date: datetime
                unlock_date: datetime
                reason: str
                description: str
                ip_id: str
            )

        """
        with self.connection.cursor() as cur:
            sql = ("SELECT `dorm_lock`.`id`,`dorm_lock`.`lock_date`,"
                   "`dorm_lock`.`unlock_date`,`dorm_lock`.`reason`,"
                   "`dorm_lock`.`description`,`dorm_lock`.`ip_id` "
                   "FROM `userinfo`"
                   "INNER JOIN `ip` ON `userinfo`.`ip_id` = `ip`.`ip`"
                   "INNER JOIN `dorm_lock` ON `dorm_lock`.`ip_id` = `ip`.`ip`"
                   "WHERE `userinfo`.`account` = %username")
            para_input = {"username": username}
            cur.execute(sql, para_input)
        return cur.fetchall()

    def set_lock(self, username: str, lock_date: str, unlock_date: str,
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
        with self.connection.cursor() as cur:
            sql = ("INSERT INTO `dorm_lock` "
                   "(`lock_date`,`unlock_date`,`reason`,`description`,`ip_id`)"
                   "SELECT %start_date,%end_date,%reason,%desc, ui.`ip_id` "
                   "FROM `userinfo` as ui "
                   "WHERE ui.`account` = %username")
            para_input = {"username": username,
                          "start_date": lock_date,
                          "end_date": unlock_date,
                          "reason": reason,
                          "desc": description}
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to insert `dorm_lock` table SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False
