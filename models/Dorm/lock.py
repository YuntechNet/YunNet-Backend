import peewee

from models import BaseModel

from ip import ip

class dorm_lock(BaseModel):
    ip          = peewee.ForeignKeyField(ip, backref='dorm_lock_ip')
    lock_date   = peewee.DateField(blank=True, null=True)
    unlock_date = peewee.DateField(blank=True, null=True)
    reason      = peewee.TextField()
    description = peewee.TextField()

    class Meta:
        table_name = 'dorm_lock'

    def __unicode__(self):
        return str(self.ip) + str(self.lock_date)
