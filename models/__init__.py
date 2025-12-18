from peewee import OperationalError
from .db import db
from .user import User
from .product import Product
from .order import Order
from .store import Store

MODELS = [User, Product, Order, Store]

def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    
    # 自動マイグレーション: store_idがない場合のみ追加
    try:
        db.execute_sql('SELECT store_id FROM product LIMIT 1;')
    except OperationalError:
        db.execute_sql('ALTER TABLE product ADD COLUMN store_id INTEGER REFERENCES store (id);')
    
    db.close()