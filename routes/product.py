from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.product import Product
from models.store import Store
from models.order import Order
from peewee import fn

# Blueprint名を 'product' に設定
product_bp = Blueprint('product', __name__, url_prefix='/products')


# routes/product.py
@product_bp.route('/')
def list():
    products = Product.select()
    # 以下の2行を削除！(すでに自動で計算される設定になっているため)
    # for product in products:
    #     product.price_with_tax = ... 

    return render_template('product_list.html', title='製品一覧', items=products)

@product_bp.route('/chart-data')
def chart_data():
    """製品の名前ラベルと在庫数をJSONで返す"""
    products = Product.select()
    labels = [p.name for p in products]
    data = [int(p.stock or 0) for p in products]
    return jsonify({'labels': labels, 'data': data})

@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        Product.create(
            name=request.form['name'],
            price=request.form['price'],
            stock=request.form.get('stock', 0),
            tax_rate=request.form.get('tax_rate', 10),
            store=request.form.get('store_id') # PR側のstore対応を採用
        )
        return redirect(url_for('product.list'))
    stores = Store.select()
    return render_template('product_add.html', stores=stores)

@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.stock = request.form.get('stock', 0)
        product.tax_rate = request.form.get('tax_rate', 10)
        product.store = request.form.get('store_id') # PR側のstore対応を採用
        product.save()
        return redirect(url_for('product.list'))

    stores = Store.select()
    return render_template('product_edit.html', product=product, stores=stores)

# @product_bp.route('/sales-chart')
@product_bp.route('/sales-chart', methods=['GET']) # ここに methods=['GET'] を追加
def sales_chart():
    """PR側で追加された新しいグラフ機能"""
    sales_data = (Store
                  .select(Store.name, fn.SUM(Order.quantity * Order.price_at_order).alias('total'))
                  .join(Product, on=(Store.id == Product.store_id))
                  .join(Order, on=(Product.id == Order.product_id))
                  .group_by(Store.id))

    labels = [s.name for s in sales_data]
    values = [float(s.total) if s.total else 0 for s in sales_data]

    return render_template('sales_chart.html', labels=labels, values=values)