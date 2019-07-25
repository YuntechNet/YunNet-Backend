import datetime

from pymysql import MySQLError
from sanic.log import logger

from Base.SQL import SQLBase


class Ip(SQLBase):
    def get_ip_by_switch(self, switch):
        with self.connection.cursor() as cur:
            # TODO rename column name
            sql = ("SELECT `ip`, `status`, `mac`, `update`, `port`"
                   ", `ip`.`port_type`, `switch`.`location` "
                   "FROM `ip` INNER JOIN `switch` "
                   "ON `switch`.`id` = `ip`.`switch_id` "
                   "WHERE `switch`.`location` = %s ")
            para_input = switch
            cur.execute(sql, switch)
            data = cur.fetchall()
            key = ['ip', 'status', 'mac', 'update', 'port', 'port_type',
                   'switch']

            dicts = [dict(zip(key, d)) for d in data]

        return dicts
        pass
