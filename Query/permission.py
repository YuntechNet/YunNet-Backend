from pymysql import MySQLError
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from sanic.log import logger

from Base.SQL import SQLBase


class Permission(SQLBase):
    def check_permission(self, username, code) -> bool:
        """Check if user have the required permission

        """

        sql = ("")
        with self.connection.cursor() as cur:
            para_input = (username, username, code, code, code)
            cur.execute(sql, para_input)
            out = cur.fetchall()
            logger.debug(out)
            if len(out) <= 0:
                return False
            else:
                return True
