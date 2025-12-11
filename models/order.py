from peewee import Model, ForeignKeyField, DateTimeField, IntegerField
from .db import db
from .user import User
from .product import Product

class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    product = ForeignKeyField(Product, backref='orders')
    # 【追加:注文数】注文数 (数量) を保存するフィールド
    order_quantity = IntegerField(default=1)  # 整数型のフィールドとして追加し、デフォルト値を1に設定
    order_date = DateTimeField()

    class Meta:
        database = db
