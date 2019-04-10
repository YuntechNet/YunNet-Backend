import peewee

from models import BaseModel

from models.User import userinfo

class announce(BaseModel):
    poster         = peewee.ForeignKeyField(userinfo, backref='announce_poster')
    title          = peewee.CharField(max_length=100, primary_key=True)
    post_time      = peewee.DateTimeField(blank=True, null=True)
    last_edit_time = peewee.DateTimeField(blank=True, null=True)
    content        = peewee.TextField()
    delete_count   = peewee.IntegerField(default=-1)
    top            = peewee.BooleanField(default=False)

    class Meta:
        table_name = 'announce'

    def __unicode__(self):
        return self.title
