from flask import Blueprint, redirect, url_for

# 最小限のスタブ: ダッシュボードが未実装でも import が通るようにする
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
def index():
    # 今は製品一覧へ誘導するだけの安全なスタブにする
    return redirect(url_for('product.list'))
