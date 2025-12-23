from peewee import Model, ForeignKeyField, IntegerField, DecimalField, CharField, DateTimeField
from .db import db
from .product import Product
from .user import User  # 「誰が」を管理するためにUserをインポート
import datetime

class Order(Model):
    # 「誰が」：顧客（User）と紐付け
    user = ForeignKeyField(User, backref='orders', verbose_name='購入者')
    
    # 「何を」：製品（Product）と紐付け
    product = ForeignKeyField(Product, backref='orders', verbose_name='製品')
    
    # 「いくつ」
    quantity = IntegerField(verbose_name='数量')
    
    # 「売上計算用」：注文時の単価を保存
    price_at_order = DecimalField(default=0, verbose_name='注文時価格')
    
    # 「いつ」：注文日時（自動で現在時刻が入るように設定）
    ordered_at = DateTimeField(default=datetime.datetime.now, verbose_name='注文日時')

    class Meta:
        database = db