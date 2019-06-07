from pymysql import MySQLError
from sanic.log import logger
from Base.SQL import SQLBase


class MAC(SQLBase):
    def get_mac(self, username: str) -> tuple:
        """get mac by username

        Args:
            username:username

        Returns:
            dict

            dict is formatted as this:
            (
                mac: str
            )

        """
        with self.connection.cursor() as cur:
            sql = (
                "SELECT ip.mac FROM userinfo "
                "INNER JOIN ip ON userinfo.ip_id = ip.ip "
                "WHERE userinfo.account = %s")
            para_input = (username)
            cur.execute(sql, para_input)

            data = cur.fetchall()
            key = ['id', 'datetime', 'content', 'account_id']

            dicts = dict(zip(key, data))

        return dicts

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
                   "SET ip.mac = %s "
                   "WHERE userinfo.account = %s ")
            para_input = (mac, account)
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
