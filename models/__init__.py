from peewee import OperationalError
from .db import db
from .user import User
from .product import Product
from .order import Order
from .store import Store

MODELS = [User, Product, Order, Store]

def initialize_database():
    db.connect()
    # 1. まずテーブルを作成（safe=Trueなので既存なら何もしない）
    db.create_tables(MODELS, safe=True)
    
    # 2. store_idカラムの存在チェックと追加
    try:
        # productテーブルにstore_idがあるか確認
        db.execute_sql('SELECT store_id FROM product LIMIT 1;')
    except OperationalError:
        print("Migrating database: Adding store_id to product table...")
        # カラムを追加。PeeweeのForeignKeyFieldに合わせて store_id として追加します
        db.execute_sql('ALTER TABLE product ADD COLUMN store_id INTEGER;')
        # 外部キーとしてのインデックスも作成しておくと安全です
        db.execute_sql('CREATE INDEX IF NOT EXISTS product_store_id ON product (store_id);')
    
    db.close()