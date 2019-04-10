import peewee

from models import BaseModel
from device import device
from models import User

class lock(BaseModel):
    ip              = peewee.CharField(max_length=32)
    mac             = peewee.CharField(max_length=18, null=True)
    department      = peewee.CharField(max_length=30)
    description     = peewee.TextField()
    lock_by_device  = peewee.CharField(max_length=32, null=True)
    lock_by         = peewee.ForeignKeyField(User.user, 
                      backref='universal_lock_lock_by')
    lock_datetime   = peewee.DateTimeField()
    unlock_by       = peewee.ForeignKeyField(User.user,
                      backref='universal_lock_unlock_by', null=True)
    unlock_datetime = peewee.DateTimeField(null=True)
    update_by       = peewee.ForeignKeyField(User.user,
                      backref='universal_lock_update_by', null=True)
    update_datetime = peewee.DateTimeField(null=True)
    lock_device     = peewee.ForeignKeyField(device, null=True)
    reason          = peewee.ForeignKeyField('lock_reason')

    class Meta:
        table_name = 'universal_lock'
