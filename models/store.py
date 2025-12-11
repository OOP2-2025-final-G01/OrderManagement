from peewee import Model, CharField, DecimalField
from .db import db

class Store(Model):
    name = CharField()

    class Meta:
        database = db