import peewee

from models import BaseModel


class unit(BaseModel):
    code            = peewee.CharField(max_length=3)
    name            = peewee.TextField()
    nickname        = peewee.TextField()

    class Meta:
        table_name = 'universal_unit'
        