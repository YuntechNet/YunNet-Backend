from pymysql import MySQLError
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from sanic.log import logger

from Base.SQL import SQLBase


class Permission(SQLBase):
    def check_permission(self, username, code) -> bool:
        """Check if user have the required permission
            
        """

        sql = ("SELECT * "
               "FROM (SELECT * "
               "FROM `user` WHERE `user`.account_id = %s) as `user` "
               "INNER JOIN `group` ON `user`.`group_id` = `group`.`code` "
               "OR `user`.`extend_group` LIKE CONCAT('%%',`group`.`code`,'%%') "
               "WHERE `user`.account_id = %s "
               "AND (`group`.per LIKE CONCAT('%%',%s,'%%') "
               "OR user.extend_per LIKE CONCAT('%%',%s,'%%')) "
               "AND NOT user.exclude_per LIKE CONCAT('%%',%s,'%%')")
        with self.connection.cursor() as cur:
            para_input = (username, username, code, code, code)
            cur.execute(sql, para_input)
            out = cur.fetchall()
            logger.debug(out)
            if len(out) <= 0:
                return False
            else:
                return True
