from aiomysql import DictCursor

from Base import SQLPool


class Token:
    @staticmethod
    async def add_token(uid, token):
        """Add token to user

        Args:
            uid:
            token:

        Returns:
            affected row.
        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "INSERT INTO `token` VALUES (%s, %s)"
                para_input = (uid, token)
                affect_row = await cur.execute(sql, para_input)

                return affect_row

    @staticmethod
    async def delete_token(token):
        """delete token

        Args:
            token:

        Returns:
            affected row.
        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor() as cur:
                sql = "DELETE FROM `token` WHERE `token` = %s"
                para_input = token
                affect_row = await cur.execute(sql, para_input)

                return affect_row

    @staticmethod
    async def get_token(token):
        """Get token

        Args:
            token:

        Returns:dict, if not found return None
            uid: int
            token: str
            timestamp: datetime

        """
        async with SQLPool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                sql = "SELECT * FROM `token` WHERE `token` = %s "
                para_input = token
                await cur.execute(sql, para_input)
                data = await cur.fetchone()
                if data is None or len(data) == 0:
                    return None

                return data
