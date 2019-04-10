import peewee

from models import BaseModel

class variable(BaseModel):
    variable    = peewee.TextField()
    value       = peewee.TextField()

    class Meta:
        table_name = 'variable'

    def __unicode__(self):
        return str(variable)
