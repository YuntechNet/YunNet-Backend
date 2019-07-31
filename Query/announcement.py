import datetime

from pymysql import MySQLError
from sanic.log import logger

from Base.SQL import SQLBase


class Announcement(SQLBase):
    def get_announcement(self, offset=0):
        """get announcement list

        get announcement limit to 10 data, use offset(page) to change page

        Args:
            offset: start from

        Returns:list with dict
        [
            {
                'title': str,
                'post_time': int,
                'last_edit_time': int,
                'content': str,
                'delete_count': int,
                'poster_id': str,
                'top': int
            },
        ]
        """
        with self.connection.cursor() as cur:
            sql = ("SELECT * FROM `announce` "
                   "ORDER BY `post_time` DESC "
                   "LIMIT %s , 10")
            para_input = (offset * 5)
            cur.execute(sql, para_input)

            data = cur.fetchall()
            key = ['title', 'post_time', 'last_edit_time', 'content',
                   'delete_count', 'poster_id', 'top']

            dicts = [dict(zip(key, d)) for d in data]

        return dicts

    def delete_announcement(self, post_id):
        """delete announcement

        Args:
            post_id: id

        Returns:bool

        """
        with self.connection.cursor() as cur:
            sql = ("DELETE FROM `announce` WHERE `title` = %s")
            para_input = (post_id)
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to delete `announce` table SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False

    def add_announcement(self, title, content, poster, top):

        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.connection.cursor as cur:
            sql = ("INSERT INTO `announce` values (%s,%s,%s,%s,-1,%s,%s)")
            para_input = (title, dt, dt, content, poster, top)
            try:
                cur.execute(sql, para_input)
                self.commit()
                return True
            except MySQLError as e:
                self.rollback()
                logger.error("got error {}, {}".format(e, e.args[0]))
                logger.error("fail to insert `announce` table SQL:{}".format(
                    cur.mogrify(sql, para_input)))
                return False
