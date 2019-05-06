from pymysql.connections import Connection

from Base.SQL import SQLBase


class User(SQLBase):
    def get_userinfo(self, username: str) -> tuple:
        """
        Get userinfo in tuple
        Tuple is formatted as this:
        (
            account: str, # can't be null
            department: str, #cant be null
            name: str, 
            lock_date: datetime,
            unlock_date: datetime, 
            launch_time: datetime,
            bed_id: string,
            ip_id: string,
            token: string,
            back_email: string,
            back_mac: string,
            last_log: datetime
        )
        """
        with self.connection.cursor() as cursor:
            sql: str = (
                "SELECT * from `userinfo` WHERE "
                "`account`=%username OR `bed_id`=%username"
            )
            cursor.execute(sql, {"username": username})
            return cursor.fetchone()

    def set_userinfo(self, userinfo: tuple) -> bool:
        """
        Set userinfo with tuple
        Tuple is formatted as this:
        (
            account: str, # can't be null
            department: str, #cant be null
            name: str, 
            lock_date: datetime,
            unlock_date: datetime, 
            launch_time: datetime,
            bed_id: string,
            ip_id: string,
            token: string,
            back_email: string,
            back_mac: string,
            last_log: datetime
        )
        """
        # todo
        return True
