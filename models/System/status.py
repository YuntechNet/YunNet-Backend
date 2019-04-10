import peewee

from models import BaseModel

class status(BaseModel):
    id          = peewee.IntegerField(primary_key=True)
    name        = peewee.CharField(max_length=20)

    class Meta:
        table_name = 'status'

    def __unicode__(self):
        return self.name
