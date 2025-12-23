from flask import Blueprint, request, redirect, url_for, flash, render_template # render_templateを追加
from models.db import db
from models.product import Product
from models.order import Order
from models.user import User # Userをインポート

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/')
def list():
    return redirect(url_for('product.list'))

@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    # --- GETのときの処理を修正 ---
    if request.method == 'GET':
        users = User.select()      # データベースから全ユーザーを取得
        products = Product.select() # データベースから全製品を取得
        return render_template('order_add.html', users=users, products=products)
    # --------------------------

    # POST処理（保存処理）
    u_id = request.form.get('user_id')    # HTMLの <select name="user_id"> から取得
    p_id = request.form.get('product_id') # HTMLの <select name="product_id"> から取得
    # 注意：HTML側の数量のname属性が "order_quantity" ならここも合わせる
    qty = int(request.form.get('quantity', 0)) 

    with db.atomic():
        product = Product.get_or_none(Product.id == p_id)
        if product and product.stock >= qty:
            product.stock -= qty
            product.save()
            # 誰が(user)買ったかも保存するように修正
            Order.create(
                user=u_id, 
                product=product, 
                quantity=qty, 
                price_at_order=product.price
            )
            flash("注文を受け付け、在庫を更新しました。")
        else:
            flash("在庫が足りないか、製品が見つかりません。")
            
    return redirect(url_for('product.list'))