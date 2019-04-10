import peewee

from models import BaseModel

from models.Dorm import ip
from models.User import group

class service(BaseModel):
    id          = peewee.IntegerField(primary_key=True)
    ip          = peewee.ForeignKeyField(ip, backref='service_ip',
                   null=False)
    description = peewee.TextField()
    own_group   = peewee.ForeignKeyField(group, backref='service_own_group',
                  null=True)
    lock        = peewee.BooleanField(default=True)

    class Meta:
        table_name = 'service'
