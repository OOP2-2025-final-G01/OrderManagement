from flask import Blueprint, render_template, request, redirect, url_for
from models import Product

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
def list():
    products = Product.select()
    # 税込価格を計算してテンプレートに渡す
    for product in products:
        product.price_with_tax = float(product.price) * (1 + product.tax_rate / 100)
    return render_template('product_list.html', title='製品一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form.get('stock', 0)
        tax_rate = request.form.get('tax_rate', 10)
        Product.create(name=name, price=price, stock=stock, tax_rate=tax_rate)
        return redirect(url_for('product.list'))
    
    return render_template('product_add.html')


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
        product.save()
        return redirect(url_for('product.list'))

    return render_template('product_edit.html', product=product)