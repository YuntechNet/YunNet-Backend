import datetime

from aiomysql import MySQLError, DictCursor
from sanic.log import logger

from Base import SQLPool


class Announcement:

    @staticmethod
    async def get_announcement():
        """get announcement list

        get announcement list only id and title

        Returns:list with dict
        [
            {
                'announcement_id': int,
                'title': str,
                `uid`: user id
            },
        ]
        """

        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "SELECT `announcement_id`,`title`, `uid` FROM `announcement`"
                await cur.execute(sql)
                data = await cur.fetchall()
                await conn.commit()

        return data

    @staticmethod
    async def get_announcement_post(id):
        """get announcement post

        get announcement post using id

        Returns:list with dict
        [
            {
                'announcement_id: int,
                'title': int,
                'content': str,
            },
        ]
        """

        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = (
                    "SELECT * "
                    "FROM `announcement` "
                    "WHERE announcement_id = %s"
                )
                await cur.execute(sql, id)
                await conn.commit()
                data = await cur.fetchone()

        return data

    # TODO(biboy1999):management logic
    # async def delete_announcement(self, post_id):
    #     """delete announcement
    #
    #     Args:
    #         post_id: id
    #
    #     Returns:bool
    #
    #     """
    #     async with SQLPool.acquire() as conn:
    #         async with conn.cursor() as cur:
    #             sql = "DELETE FROM `announce` WHERE `title` = %s"
    #             para_input = post_id
    #             try:
    #                 await cur.execute(sql, para_input)
    #                 await conn.commit()
    #                 return True
    #             except MySQLError as e:
    #                 await conn.rollback()
    #                 logger.error("got error {}, {}".format(e, e.args[0]))
    #                 logger.error(
    #                     "fail to delete `announce` table SQL:{}".format(
    #                         await cur.mogrify(sql, para_input)
    #                     )
    #                 )
    #                 return False
    #
    # async def add_announcement(self, title, content, poster, top):
    #
    #     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #     async with SQLPool.acquire() as conn:
    #         async with conn.cursor() as cur:
    #             sql = "INSERT INTO `announce` values (%s,%s,%s,%s,-1,%s,%s)"
    #             para_input = (title, dt, dt, content, poster, top)
    #             try:
    #                 await cur.execute(sql, para_input)
    #                 await conn.commit()
    #                 return True
    #             except MySQLError as e:
    #                 await conn.rollback()
    #                 logger.error("got error {}, {}".format(e, e.args[0]))
    #                 logger.error(
    #                     "fail to insert `announce` table SQL:{}".format(
    #                         await cur.mogrify(sql, para_input)
    #                     )
    #                 )
    #                 return False
