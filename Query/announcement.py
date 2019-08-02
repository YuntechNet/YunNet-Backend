import datetime

from aiomysql import MySQLError
from sanic.log import logger

from Base import SQLPool


class Announcement():
    async def get_announcement(self, offset=0):
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
        
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = ("SELECT * FROM `announce` "
                    "ORDER BY `post_time` DESC "
                    "LIMIT %s , 10")
                para_input = (offset * 5)
                await cur.execute(sql, para_input)

                data = await cur.fetchall()
                key = ['title', 'post_time', 'last_edit_time', 'content',
                    'delete_count', 'poster_id', 'top']

                dicts = [dict(zip(key, d)) for d in data]

        return dicts

    async def delete_announcement(self, post_id):
        """delete announcement

        Args:
            post_id: id

        Returns:bool

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = ("DELETE FROM `announce` WHERE `title` = %s")
                para_input = (post_id)
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    await conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error("fail to delete `announce` table SQL:{}".format(
                        await cur.mogrify(sql, para_input)))
                    return False

    async def add_announcement(self, title, content, poster, top):

        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = ("INSERT INTO `announce` values (%s,%s,%s,%s,-1,%s,%s)")
                para_input = (title, dt, dt, content, poster, top)
                try:
                    await cur.execute(sql, para_input)
                    await conn.commit()
                    return True
                except MySQLError as e:
                    await conn.rollback()
                    logger.error("got error {}, {}".format(e, e.args[0]))
                    logger.error("fail to insert `announce` table SQL:{}".format(
                        await cur.mogrify(sql, para_input)))
                    return False
