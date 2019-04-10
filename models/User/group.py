import peewee

from models import BaseModel

class group(BaseModel):
    code        = peewee.CharField(max_length=4, blank=False, primary_key=True)
    name        = peewee.TextField()
    per         = peewee.TextField(null=True)
    full_name   = peewee.TextField(null=True)

    class Meta:
        table_name = 'group'
