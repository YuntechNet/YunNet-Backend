from pymysql.connections import Connection

from Base.SQL import SQLBase

class User(SQLBase):
    def get_netflow(self, username: str) -> list:
        #todo
        return [()]
