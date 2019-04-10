import peewee

from models import BaseModel

class cisco_log(BaseModel):
    datetime        = peewee.DateTimeField()
    log             = peewee.TextField()

    class Meta:
        table_name = 'cisco_log'
