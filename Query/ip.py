import datetime

from pymysql import MySQLError
from sanic.log import logger

from Base.SQL import SQLBase


class Ip(SQLBase):
    # TODO(biboy1999): WIP management logic
    # def get_ip_by_switch(self, switch):
    #     with self.connection.cursor() as cur:
    #         sql = ("SELECT `ip`, `status`, `mac`, `update`, `port`"
    #                ", `ip`.`port_type`, `switch`.`location` "
    #                "FROM `ip` INNER JOIN `switch` "
    #                "ON `switch`.`id` = `ip`.`switch_id` "
    #                "WHERE `switch`.`location` = %s ")
    #         para_input = switch
    #         cur.execute(sql, switch)
    #         data = cur.fetchall()
    #         key = ['ip', 'status', 'mac', 'update', 'port', 'port_type',
    #                'switch']
    #
    #         dicts = [dict(zip(key, d)) for d in data]
    #
    #     return dicts

    def get_user_ip_mac(self, uid):
        with self.connection.cursor() as cur:
            sql = ("SELECT i.`ip`, i.`mac` "
                   "FROM `ip` as i "
                   "INNER JOIN `bed` as b ON i.`ip` = b.`ip` "
                   "INNER JOIN `user` as u ON b.`bed` = u.`bed` "
                   "WHERE u.`uid` = %s ")
            para_input = uid
            cur.execute(sql, para_input)
            data = cur.fetchone()

            key = ["ip", "mac"]
            dicts = dict(zip(data, key))

        return dicts
