from pymysql import MySQLError
from sanic.log import logger

from Base.SQL import SQLBase


class log(SQLBase):
    def get_log(self, offset=0):
        with self.connection.cursor() as cur:
            sql = ("SELECT * FROM `log` "
                   "ORDER BY `datetime` DESC "
                   "LIMIT %s,100")
            para_input = (offset * 100)
            cur.execute(sql, para_input)
        return cur.fetchall()

    def delete_log(self, log_id):
        with self.connection.cursor() as cur:
            sql = ("DELETE FROM `log` WHERE `id` = 123")
            para_input = (log_id)
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to delete `log` table SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False
