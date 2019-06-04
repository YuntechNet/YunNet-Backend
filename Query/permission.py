from pymysql import MySQLError
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from sanic.log import logging

from Base.SQL import SQLBase


class Permission(SQLBase):
    def check_permission(self, username, code) -> bool:
        """Check if user have the required permission
            
        """
        sql = ("SELECT * "
               "FROM user "
               "INNER JOIN `group` ON user.group_id = `group`.code "
               "OR user.extend_group LIKE CONCAT('%',`group`.code,'%') "
               "WHERE user.account_id = %username "
               "AND `group`.per "
               "LIKE CONCAT('%',%code,'%') "
               "OR user.extend_per "
               "LIKE CONCAT('%',%code,'%') "
               "AND NOT user.exclude_per "
               "LIKE CONCAT('%',%code,'%')")
        with self.connection.cursor() as cur:
            para_input = {'username': username, 'code': code}
            cur.execute(sql, para_input)
            out = cur.fetchall()
            if out.length <= 0:
                return False
            else:
                return True
