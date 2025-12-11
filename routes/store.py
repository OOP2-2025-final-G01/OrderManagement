from flask import Blueprint, render_template, request, redirect, url_for
from models.store import Store

# Blueprintの作成
store_bp = Blueprint('store', __name__, url_prefix='/stores')


@store_bp.route('/')
def list():
    stores = Store.select()
    return render_template('store_list.html', title='店舗一覧', items=stores)


@store_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        Store.create(name=name)
        return redirect(url_for('store.list'))
    
    return render_template('store_add.html')


@store_bp.route('/edit/<int:store_id>', methods=['GET', 'POST'])
def edit(store_id):
    store = Store.get_or_none(Store.id == store_id)
    if not store:
        return redirect(url_for('store.list'))

    if request.method == 'POST':
        store.name = request.form['name']
        store.save()
        return redirect(url_for('store.list'))

    return render_template('store_edit.html', store=store)