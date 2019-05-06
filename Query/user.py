from pymysql.connections import Connection

from Base.SQL import SQLBase

class User(SQLBase):
    def new_user(self, username:str, password: str) -> tuple:
        #todo
        return ()

    def get_password(self, username: str) -> tuple:
        #todo
        return ()

    def set_password(self, username: str, password: str) -> tuple:
        #todo
        return ()

