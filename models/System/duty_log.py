import peewee

from models import BaseModel

class duty_log(BaseModel):
    datetime    = peewee.DateTimeField()
    content     = peewee.TextField()

    class Meta:
        table_name = 'duty_log'

    def __unicode__(self):
        return str(self.datetime)