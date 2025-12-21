# ターミナルで"pip install matplotlib japanize-matplotlib"
import io
import base64
import matplotlib
matplotlib.use('Agg')  # GUIのない環境用
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
def list():
    search_query = request.args.get('search')

    # 1. データ取得
    if search_query:
        query = User.select().where(User.phone_number.contains(search_query))
    else:
        query = User.select()

    # 【重要】クエリ結果をリスト化（グラフ集計とHTML表示で2回ループするため）
    users = [user for user in query]

    # 2. グラフ生成ロジック (検索結果に基づいて集計)
    age_counts = {}
    for user in users:
        try:
            if not user.age:
                continue
            age = int(user.age)
            generation = (age // 10) * 10
            
            if generation not in age_counts:
                age_counts[generation] = 0
            age_counts[generation] += 1
        except (ValueError, TypeError):
            continue

    plot_url = None
    if age_counts:
        # データを年代順にソート
        sorted_generations = sorted(age_counts.items())
        labels = [f"{gen}代" for gen, count in sorted_generations]
        values = [count for gen, count in sorted_generations]

        # グラフ描画
        plt.figure(figsize=(6, 4)) # サイズ調整(少し横長に)
        # 背景を透明にするとWebデザインに馴染みやすい
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False)
        plt.title(f'年齢分布 ({len(users)}件)')
        plt.axis('equal') 
        
        # 保存とエンコード
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight') # 余白を削除して保存
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

    # 3. テンプレートへ渡す
    return render_template('user_list.html', 
                           title='ユーザー一覧', 
                           items=users, 
                           search_query=search_query, 
                           plot_url=plot_url)

@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form.get('phone_number') # フォームから電話番号から取得
        User.create(name=name, age=age, phone_number=phone)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.phone_number = request.form.get('phone_number') # 電話番号更新
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)