import peewee

from models import BaseModel

from ip import ip

class bed(BaseModel):
    bed         = peewee.CharField(max_length=9, primary_key=True)
    type        = peewee.IntegerField(default=0)
    portal      = peewee.CharField(max_length=9, null=True)
    ip          = peewee.ForeignKeyField(ip, backref='bed_ip', default=None)

    class Meta:
        table_name = 'bed'

    def __unicode__(self):
        return self.bed
