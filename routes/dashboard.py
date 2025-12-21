import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib
from flask import Blueprint, render_template, request, redirect, url_for
from models import User, Product

# 単一の Blueprint にまとめる（重複定義を排除）
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
def index():
    # ダッシュボードページ（必要なら製品一覧への案内を含める）
    # 今は user 年齢分布を表示するテンプレートをレンダリング
    users = list(User.select())
    age_counts = {}
    for user in users:
        try:
            if not user.age:
                continue
            age = int(user.age)
            generation = (age // 10) * 10
            age_counts[generation] = age_counts.get(generation, 0) + 1
        except (ValueError, TypeError):
            continue

    plot_url = None
    if age_counts:
        sorted_generations = sorted(age_counts.items())
        labels = [f"{gen}代" for gen, _ in sorted_generations]
        values = [count for _, count in sorted_generations]

        plt.figure(figsize=(6, 4))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False)
        plt.title(f'年齢分布 ({len(users)}件)')
        plt.axis('equal')

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

    return render_template('dashboard.html', plot_url=plot_url)


@dashboard_bp.route('/age-chart')
def age_chart():
    """年齢分布の円グラフを base64 エンコード文字列で返す（JSON）。"""
    users = list(User.select())
    age_counts = {}
    for user in users:
        try:
            if not user.age:
                continue
            age = int(user.age)
            generation = (age // 10) * 10
            age_counts[generation] = age_counts.get(generation, 0) + 1
        except (ValueError, TypeError):
            continue

    plot_url = None
    if age_counts:
        sorted_generations = sorted(age_counts.items())
        labels = [f"{gen}代" for gen, _ in sorted_generations]
        values = [count for _, count in sorted_generations]

        plt.figure(figsize=(6, 4))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False)
        plt.title(f'年齢分布 ({len(users)}件)')
        plt.axis('equal')

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

    return {'plot_url': plot_url}
