import peewee

from models import BaseModel

class device(BaseModel):
    name            = peewee.TextField()
    ip              = peewee.CharField(max_length=45)

    class Meta:
        table_name = 'universal_device'
