from flask import Blueprint, request, redirect, url_for, flash
from models.db import db
from models.product import Product
from models.order import Order

order_bp = Blueprint('order', __name__, url_prefix='/orders')

# order.list への BuildError 回避
@order_bp.route('/')
def list():
    return redirect(url_for('product.list'))

@order_bp.route('/create', methods=['POST'])
def create():
    p_id = request.form.get('product_id')
    qty = int(request.form.get('quantity', 0))

    with db.atomic():
        product = Product.get_or_none(Product.id == p_id)
        if product and product.stock >= qty:
            product.stock -= qty
            product.save()
            # 売上のために、現在の単価を price_at_order に保存
            Order.create(product=product, quantity=qty, price_at_order=product.price)
            flash("注文を受け付け、在庫を更新しました。")
    return redirect(url_for('product.list'))