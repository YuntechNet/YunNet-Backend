from pymysql.connections import Connection

from Base.SQL import SQLBase

class User(SQLBase):
    def create_account(self, username: str) -> bool:
        #todo
        return bool
