from pymysql.connections import Connection

from Base.SQL import SQLBase

class User(SQLBase):
    def get_mac(self, username: str) -> tuple:
        #todo
        return ()

    def set_mac(self, userinfo: tuple) -> bool:
        #todo
        return True
