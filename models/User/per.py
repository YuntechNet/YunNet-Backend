import peewee

from models import BaseModel

class per(BaseModel):
    code        = peewee.CharField(max_length=4, primary_key=True)
    name        = peewee.TextField()
    full_name   = peewee.TextField(null=True)

    class Meta:
        table_name = 'per'
