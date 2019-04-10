import peewee

from models import BaseModel

from ip import ip

class switch(BaseModel):
    id               = peewee.IntegerField(primary_key=True)
    ip               = peewee.ForeignKeyField(ip, backref='switch_ip',
                       null=True)
    upper_id         = peewee.IntegerField(default=0)
    upper_port       = peewee.IntegerField(default=0)
    upper_port_type  = peewee.IntegerField(default=0)
    location         = peewee.CharField(max_length=10, null=True)
    telnet_passwd    = peewee.CharField(max_length=30)
    account          = peewee.CharField(max_length=30)
    vlan             = peewee.IntegerField()
    machine_type     = peewee.IntegerField(default=0)
    port_description = peewee.TextField()
    port_type        = peewee.TextField()
    MB_Serial_Number = peewee.CharField(max_length=15)

    class Meta:
        table_name = 'switch'
