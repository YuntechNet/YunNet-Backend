import peewee

from models import BaseModel

class flow_log(BaseModel):
    id              = peewee.AutoField(primary_key=True, db_index=True)
    ip              = peewee.CharField(max_length=45, blank=False, null=False)
    stamp           = peewee.DateTimeField(auto_now_add=True, null=False)
    flow            = peewee.BigIntegerField(null=False)

    class Meta:
        table_name = 'flow_log'
