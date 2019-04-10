from peewee import Model, DatabaseProxy

database_proxy = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy
