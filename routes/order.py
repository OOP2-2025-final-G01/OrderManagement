from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']

        #【追加】'order_quantity' の値を取得
        # 'order_quantity'がPOSTデータに含まれていない場合や不正な場合はデフォルトで1にする
        try:
            order_quantity = int(request.form.get('order_quantity', 1))
        except ValueError:
            order_quantity = 1  # 整数に変換できない場合はデフォルト値を使用  
            
        order_date = datetime.now()

        Order.create(user=user_id, product=product_id, quantity=order_quantity, order_date=order_date)
        return redirect(url_for('order.list'))
    
    users = User.select()
    products = Product.select()
    return render_template('order_add.html', users=users, products=products)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        order.user = request.form['user_id']
        order.product = request.form['product_id']

        #【追加】 'order_quantity' の値を取得し、orderオブジェクトに設定
        try:
            order_quantity = int(request.form.get('order_quantity', 1))
        except ValueError:
            order_quantity = 1 
            
        order.order_quantity = order_quantity # order.order_quantity に値を設定

        order.save()
        return redirect(url_for('order.list'))

    users = User.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, users=users, products=products)
