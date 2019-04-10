import peewee

from models import BaseModel

class cron_log(BaseModel):
    description     = peewee.TextField()
    datetime        = peewee.DateTimeField()

    class Meta:
        table_name = 'cron_log'
