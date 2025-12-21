import io
import base64
import matplotlib
matplotlib.use('Agg')  # サーバーサイドでの描画に必須
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Blueprint, render_template
from peewee import fn
from models.user import User
from models.product import Product
from models.store import Store
from models.order import Order

# --- 1. Blueprintの定義（これが NameError の原因でした） ---
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def index():
    """/dashboard/ に直接アクセスした際の処理"""
    return render_template('dashboard.html', plot_url=None) 

@dashboard_bp.route('/age-chart')
def age_chart():
    """
    年齢分布の円グラフを JSON で返す関数
    index.html の JavaScript (fetch('/dashboard/age-chart')) から呼ばれます
    """
    users = list(User.select())
    age_counts = {}
    for user in users:
        try:
            if not user.age: continue
            # 年齢から世代（10代, 20代...）を計算
            age = int(user.age)
            generation = (age // 10) * 10
            age_counts[generation] = age_counts.get(generation, 0) + 1
        except: continue

    plot_url = None
    if age_counts:
        plt.close('all') # 描画リセット
        plt.figure(figsize=(6, 4))
        sorted_gen = sorted(age_counts.items())
        labels = [f"{g}代" for g, _ in sorted_gen]
        values = [c for _, c in sorted_gen]

        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')

        # 画像をBase64文字列に変換
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

    # JavaScriptが読み取れる形式で返す
    return {"plot_url": plot_url}

# --- 2. 店舗別売上データ取得用（これを追加すると、index.htmlに売上グラフも出せます） ---
@dashboard_bp.route('/sales-chart-data')
def sales_chart_data():
    """店舗別の売上合計を計算して JSON で返す"""
    try:
        # Store, Product, Order を繋いで、店舗名ごとに (数量 * 単価) を合計
        sales_data = (Store
                      .select(Store.name, fn.SUM(Order.quantity * Order.price_at_order).alias('total'))
                      .join(Product, on=(Store.id == Product.store_id))
                      .join(Order, on=(Product.id == Order.product_id))
                      .group_by(Store.id))
        
        return {
            "labels": [s.name for s in sales_data],
            "values": [float(s.total) for s in sales_data]
        }
    except Exception as e:
        print(f"Sales Data Error: {e}")
        return {"labels": [], "values": []}