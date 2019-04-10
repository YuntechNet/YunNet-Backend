import peewee

from models.model import BaseModel

class segment(BaseModel):
    v4              = peewee.CharField(max_length=11)
    assignment      = peewee.TextField(null=True)
    description     = peewee.TextField(null=True)

    class Meta:
        table_name = 'universal_segment'
