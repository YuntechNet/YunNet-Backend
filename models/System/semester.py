import peewee

from models import BaseModel

class semester(BaseModel):
    name        = peewee.TextField()
    begin_date  = peewee.DateField()
    end_date    = peewee.DateField()
    schedule    = peewee.TextField(default='')

    class Meta:
        table_name = 'semester'

    def __unicode__(self):
        return str(self.name)
