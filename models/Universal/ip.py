import peewee

from models import BaseModel

from segment import segment

class ip(BaseModel):
    segment         = peewee.ForeignKeyField(segment)
    group           = peewee.ForeignKeyField('User.group', 
                      backref='universal_group', null=True)
    ip              = peewee.IntegerField()

    class Meta:
        table_name = 'universal_ip'
