import peewee

from models import BaseModel

class lock_reason(BaseModel):
    code            = peewee.CharField(max_length=1)
    description     = peewee.TextField()

    class Meta:
        table_name = 'lock_reason'
