import peewee

from models import BaseModel

class log(BaseModel):
    datetime    = peewee.DateTimeField()
    account     = peewee.ForeignKeyField('User.user', backref='log_account')
    content     = peewee.TextField()

    class Meta:
        table_name = 'log'
