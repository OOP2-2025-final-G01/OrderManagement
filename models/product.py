from peewee import Model, CharField, DecimalField, IntegerField
from .db import db

class Product(Model):
    name = CharField()
    price = DecimalField()
    stock = IntegerField(default=0)

    class Meta:
        database = db