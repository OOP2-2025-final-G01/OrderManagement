from flask import Blueprint, render_template, request, redirect, url_for
from peewee import fn
from models import Product, Store

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def list():
    products = Product.select()
    # 手動計算(product.price_with_tax = ...)を削除し属性エラーを回避
    return render_template('product_list.html', title='製品一覧', items=products)

@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        Product.create(
            name=request.form['name'],
            price=request.form['price'],
            stock=request.form.get('stock', 0),
            tax_rate=request.form.get('tax_rate', 10),
            store=request.form.get('store_id')
        )
        return redirect(url_for('product.list'))
    stores = Store.select()
    return render_template('product_add.html', stores=stores)

@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.stock = request.form.get('stock', 0)
        product.tax_rate = request.form.get('tax_rate', 10)
        product.store = request.form.get('store_id')
        product.save()
        return redirect(url_for('product.list'))
    stores = Store.select()
    return render_template('product_edit.html', product=product, stores=stores)

@product_bp.route('/chart')
def sales_chart():
    # 店舗ごとの在庫総額を集計
    stats = (Product
             .select(Store.name, fn.SUM(Product.price * Product.stock).alias('total'))
             .join(Store)
             .group_by(Store.id))
    labels = [s.store.name for s in stats]
    values = [float(s.total) for s in stats]
    return render_template('sales_chart.html', labels=labels, values=values)