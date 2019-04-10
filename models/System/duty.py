import peewee

from models import BaseModel

class duty(BaseModel):
    date        = peewee.DateField(null=False)
    schedule    = peewee.TextField()

    class Meta:
        table_name = 'duty'

    def __unicode__(self):
        return str(self.semester)
