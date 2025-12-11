from peewee import Model, CharField, IntegerField
from .db import db

class User(Model):
    name = CharField()
    age = IntegerField()
    phone_number = CharField(null = True) # 電話番号

    class Meta:
        database = db