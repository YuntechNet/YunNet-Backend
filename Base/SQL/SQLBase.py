import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from config import SQL_CREDENTIALS


class SQLBase:
    """
    Creates connection object from config.py at root directory
    """

    def __init__(self):
        self.connection = pymysql.connect(host=SQL_CREDENTIALS['host'],
                                          port=SQL_CREDENTIALS['port'],
                                          user=SQL_CREDENTIALS['user'],
                                          password=SQL_CREDENTIALS['password'],
                                          database=SQL_CREDENTIALS['db'])

    def __del__(self):
        if self.connection.open:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
