from peewee import Model, ForeignKeyField, IntegerField, DecimalField
from .db import db
from .product import Product

class Order(Model):
    product = ForeignKeyField(Product, backref='orders')
    quantity = IntegerField()
    # 売上計算用：注文時の単価を保存
    price_at_order = DecimalField(default=0)

    class Meta:
        database = db