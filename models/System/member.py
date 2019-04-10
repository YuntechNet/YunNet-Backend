import peewee

from models import BaseModel

class member(BaseModel):
    name        = peewee.CharField(max_length=20)
    account     = peewee.CharField(max_length=20)
    student_id  = peewee.CharField(max_length=20)
    birthday    = peewee.DateField()
    phone       = peewee.CharField(max_length=11)
    serial      = peewee.TextField()
    graduate    = peewee.IntegerField(default=0)

    class Meta:
        table_name = 'member'

    def __unicode__(self):
        return str(self.name)
