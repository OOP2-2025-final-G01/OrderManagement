from .user import user_bp
from .product import product_bp
from .order import order_bp
from .store import store_bp
from .dashboard import dashboard_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  order_bp, # これが抜けているとルーティングエラーになります
  store_bp,
  dashboard_bp
]
