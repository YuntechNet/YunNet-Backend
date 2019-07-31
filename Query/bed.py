from pymysql import MySQLError
from sanic.log import logger

from Base.SQL import SQLBase


class Bed(SQLBase):
    def get_user_bed_info(self, uid):
        '''

        Args:
            uid: user_id

        Returns:
            dict
            {
                bed: string
                portal: string
                ip: string

            }

        '''
        with self.connection.cursor() as cur:
            sql = ("SELECT b.`bed`,b.`portal` "
                   "FROM `bed` as b "
                   "INNER JOIN `user` as u ON b.`bed` = u.`bed` "
                   "WHERE u.`uid` = %s ")
            para_input = uid
            cur.execute(sql, para_input)
            data = cur.fetchone()

            key = ["bed", "portal"]
            dicts = dict(zip(data, key))

        return dicts
