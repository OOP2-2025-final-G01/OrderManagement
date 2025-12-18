from flask import Blueprint, render_template, request, redirect, url_for
from models.product import Product
from models.store import Store
from models.order import Order
from peewee import fn

# Blueprint名を 'product' に設定
product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def list():
    products = Product.select()
    return render_template('product_list.html', items=products)

@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    """BuildError(product.add)を解決する関数"""
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
    """BuildError(product.edit)を解決する関数。引数名を product_id に固定"""
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.stock = request.form.get('stock', 0)
        product.store = request.form.get('store_id')
        product.save()
        return redirect(url_for('product.list'))

    stores = Store.select()
    return render_template('product_edit.html', product=product, stores=stores)

@product_bp.route('/sales-chart')
def sales_chart():
    """店舗別の売上（数量 * 注文時単価）を集計"""
    sales_data = (Store
                  .select(Store.name, fn.SUM(Order.quantity * Order.price_at_order).alias('total'))
                  .join(Product, on=(Store.id == Product.store_id))
                  .join(Order, on=(Product.id == Order.product_id))
                  .group_by(Store.id))

    labels = [s.name for s in sales_data]
    values = [float(s.total) if s.total else 0 for s in sales_data]

    return render_template('sales_chart.html', labels=labels, values=values)