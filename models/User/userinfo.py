import peewee

from models import BaseModel

from models.Dorm import bed as dorm_bed
from models.Dorm import ip as dorm_ip

class userinfo(BaseModel):
    account     = peewee.CharField(max_length=20, primary_key=True)
    bed         = peewee.ForeignKeyField(dorm_bed, backref='userinfo_bed',
                  null=True)
    ip          = peewee.ForeignKeyField(dorm_ip, backref='userinfo_ip',
                  null=True)
    department  = peewee.CharField(max_length=30)
    name        = peewee.CharField(max_length=20)
    lock_date   = peewee.DateField(blank=True, null=True)
    unlock_date = peewee.DateField(blank=True, null=True)
    launch_time = peewee.DateTimeField(blank=True, null=True)
    token       = peewee.CharField(max_length=64, null=True, blank=False, 
                  unique=True)
    back_email  = peewee.CharField(max_length=150, blank=False, null=True)
    back_mac    = peewee.CharField(max_length=18, null=True)
    last_log    = peewee.DateTimeField(blank=True, null=True)

    class Meta:
        table_name = 'userinfo'

    def __unicode__(self):
        return self.account
