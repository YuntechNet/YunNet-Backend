import peewee

from models import BaseModel

class global_lock(BaseModel):
    ip          = peewee.CharField(max_length=32)
    lock_date   = peewee.DateField(blank=True, null=True)
    unlock_date = peewee.DateField(blank=True, null=True)
    reason      = peewee.TextField()
    description = peewee.TextField()

    class Meta:
        table_name = 'global_lock'

    def __unicode__(self):
        return str(self.ip) + str(self.lock_date)
