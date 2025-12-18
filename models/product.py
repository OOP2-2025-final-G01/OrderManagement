from peewee import Model, CharField, DecimalField, IntegerField, ForeignKeyField
from .db import db
from .store import Store

class Product(Model):
    name = CharField()
    price = DecimalField()
    stock = IntegerField(default=0)
    tax_rate = IntegerField(default=10)
    # 店舗との紐付け
    store = ForeignKeyField(Store, backref='products', null=True)

    class Meta:
        database = db

    @property
    def price_with_tax(self):
        return float(self.price) * (1 + self.tax_rate / 100)