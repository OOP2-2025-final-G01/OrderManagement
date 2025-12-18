# アプリ名: 販売管理システム

概要:
顧客・商品・注文情報を一元管理できる「販売管理システム」です。 ユーザーと製品の基本データ登録に加え、それらを紐付けた注文処理や店舗情報の管理が可能です。また、電話番号による顧客検索など、現場での利便性を考慮した機能を備えています。
【主な機能】
顧客管理： 名前・年齢・電話番号の登録および、電話番号によるスムーズな顧客検索
製品管理： 製品名・価格・在庫状況のリアルタイムな登録・管理
注文管理： 「誰が」「何を」「いつ」「いくつ」購入したかの履歴管理
店舗管理： 販売拠点となる店舗情報の登録・整理


## アピールポイント

この部分に、発表に替わる内容を書きます。
アプリケーション動作のサンプル動画などを貼り付けられると良いです。
※動画の貼り付けは、GIFアニメーションなどでも可です。
たくさんの顧客データの中から名前だけで探すのは大変です。そこで、実店舗のポイントカード管理などのように、電話番号で即座にユーザーを特定できる検索機能を実装しました。
ユーザー、製品、注文、店舗というバラバラなデータを紐付けました。「いつ、どの店で、誰が、何を買ったか」を記録できる設計にしています。
Matplotlib を使ってグラフ化する機能を導入しました。

## 動作条件: require

> 動作に必要な条件を書いてください。
- Python 3.13 以上
- 必要なライブラリ: Flask, Peewee, Matplotlib, japanize-matplotlib

```bash
python 3.13 or higher

# python lib
Flask==3.0.3
peewee==3.17.7
```

## 使い方: usage

> 以下のコマンドをターミナルの作業ディレクトリで実行します。
```bash
$ rm -f my_database.db && python app.py
$ pip install Flask==3.0.3 peewee==3.17.7
$ rm -f my_database.db
$ timeout 5 python app.py || true
$ python -c "from models import initialize_database; initialize_database(); print('Database initialized successfully!')"
$ pip install matplotlib
$ pip install japanize-matplotlib

# Try accessing "http://localhost:8080" in your browser.
```

```bash
$ python app.py
# Try accessing "http://localhost:8080" in your browser.
```
