import peewee

from models import BaseModel

from models.User import userinfo

class user(BaseModel):
    account      = peewee.ForeignKeyField(userinfo, unique=True, 
                   backref='user_account', primary_key=True)
    passwd       = peewee.CharField(max_length=64, null=True)
    group        = peewee.ForeignKeyField('User.group', backref='user_group', 
                   null=True)
    extend_group = peewee.TextField(default='[]', null=False)
    extend_per   = peewee.TextField(default='[]', null=False)
    exclude_per  = peewee.TextField(default='[]', null=False)

    class Meta:
        table_name = 'user'

    def __unicode__(self):
        return self.account
