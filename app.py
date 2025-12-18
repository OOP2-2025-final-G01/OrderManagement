from flask import Flask, render_template
from models import initialize_database, Product
from routes import blueprints
import os

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # 製品ごとの在庫データを取得してホームに渡す
    products = Product.select()
    labels = [p.name for p in products]
    data = [int(p.stock or 0) for p in products]
    return render_template('index.html', labels=labels, data=data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
