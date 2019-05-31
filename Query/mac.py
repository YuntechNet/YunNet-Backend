from pymysql import MySQLError
from pymysql.connections import Connection
from sanic.log import logger

from Base.SQL import SQLBase


class MAC(SQLBase):
    def get_mac(self, username: str) -> tuple:
        """get mac by username

        Args:
            username:username

        Returns:
            tuple

            Tuple is formatted as this:
            (
                mac: str
            )

        """
        with self.connection.cursor() as cur:
            sql = (
                "SELECT ip.mac FROM userinfo "
                "INNER JOIN ip ON userinfo.ip_id = ip.ip "
                "WHERE userinfo.account = %username")
            para_input = {"username": username}
            cur.execute(sql, para_input)
            return cur.fetchone()

    def set_mac(self, account: str, mac: str) -> bool:
        """Set mac by account_id

        Args:
            account: account_id
            mac:mac address

        Returns:
            bool, If set success return True, if catch error return False.

        """
        with self.connection.cursor() as cur:
            sql = ("UPDATE ip "
                   "INNER JOIN userinfo ON userinfo.ip_id = ip.ip "
                   "SET ip.mac = %mac "
                   "WHERE userinfo.account = %account ")
            para_input = {"mac": mac,
                          "account": account}
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to udpate `ip` table SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False
