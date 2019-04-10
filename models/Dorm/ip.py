import peewee

from models import BaseModel

from switch import switch

class ip(BaseModel):
    ip          = peewee.CharField(max_length=32, primary_key=True)
    status      = peewee.IntegerField(default=0)
    mac         = peewee.CharField(max_length=18, null=True)
    update      = peewee.IntegerField(default=0)
    switch      = peewee.ForeignKeyField(switch, backref='ip_switch', null=True)
    port        = peewee.IntegerField(default=0)
    port_type   = peewee.IntegerField(default=0)

    class Meta:
        table_name = 'ip'

    def __unicode__(self):
        return self.ip
