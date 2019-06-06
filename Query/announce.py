from Base.SQL import SQLBase


class Announce(SQLBase):
    def get_announcement(self, offset=0):
        """get announcement list

        get announcement limit to 10 data, use offset(page) to change page

        Args:
            offset: start from

        Returns:

        """
        with self.connection.cursor() as cur:
            sql = ("SELECT * FROM `announce` "
                   "ORDER BY `post_time` DESC "
                   "LIMIT %s , 10")
            para_input = (offset * 5)
            cur.execute(sql, para_input)
        return cur.fetchall()
