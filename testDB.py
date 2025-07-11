import os
import sqlite3
import database as db

# テスト用のデータベースファイル名を設定
TEST_DATABASE_FILE = 'test_terminal_x.db'
db.DATABASE_FILE = TEST_DATABASE_FILE

def setup_database():
    """
    テスト用のデータベースを初期化する。
    schema.sqlファイルを読み込んでテーブルを作成し、初期データを投入する。
    """
    # 既存のテストDBファイルがあれば削除
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)
        
    conn = sqlite3.connect(TEST_DATABASE_FILE)
    cursor = conn.cursor()

    # --- schema.sqlファイルを読み込んで実行 ---
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print(" -> 'schema.sql' を正常に読み込んで実行しました。")
    except FileNotFoundError:
        print("\n❌ エラー: 'schema.sql' が見つかりません。テストを実行できません。")
        print("このテストスクリプトと同じディレクトリに 'schema.sql' を配置してください。")
        exit(1) # ファイルが見つからない場合はテストを中止
    
    # FOREIGN KEY制約を有効にする
    cursor.execute('PRAGMA foreign_keys = ON;')

    conn.commit()
    conn.close()
    print(f"--- テストデータベース '{TEST_DATABASE_FILE}' をセットアップしました ---")


def test_user_operations():
    """ユーザー関連のCRUD操作をテストする"""
    print("\n[テスト開始] ユーザー操作")
    
    # 1. ユーザー作成
    print("1. 新規ユーザー 'testuser' を作成します...")
    user = db.create_user('testuser', 'password123')
    assert user is not None
    assert user['username'] == 'testuser'
    print(f" -> 成功: ユーザーID {user['id']} で作成されました。")

    # 2. パスワード検証
    print("2. パスワードを検証します...")
    assert db.verify_password('testuser', 'password123') is True
    print(" -> 成功: 正しいパスワードで認証OK。")
    assert db.verify_password('testuser', 'wrongpassword') is False
    print(" -> 成功: 間違ったパスワードで認証NG。")

    # 3. 既存ユーザー名の重複作成テスト
    print("3. 重複ユーザー名 'testuser' で作成を試みます...")
    duplicate_user = db.create_user('testuser', 'password123')
    assert duplicate_user is None
    print(" -> 成功: 重複作成は失敗しました。")
    
    print("[テスト完了] ユーザー操作")
    return user # 他のテストで使うためにユーザー情報を返す


def test_product_operations():
    """商品関連のCRUD操作をテストする"""
    print("\n[テスト開始] 商品操作")
    
    # schema.sqlで初期データが投入されていることを前提とする
    
    # 1. 全商品取得
    print("1. 全商品を取得します...")
    products = db.get_all_products()
    assert len(products) >= 4 # schema.sqlで4件の商品を投入
    print(f" -> 成功: {len(products)}件の商品を取得しました。")

    # 2. IDで商品取得
    print("2. ID=1の商品を取得します...")
    product = db.get_product_by_id(1)
    assert product is not None
    assert product['name'] == 'Item_X123'
    print(f" -> 成功: 商品'{product['name']}'を取得しました。")

    print("[テスト完了] 商品操作")


def test_message_operations(user1):
    """メッセージ関連のCRUD操作をテストする"""
    print("\n[テスト開始] メッセージ操作")
    
    # schema.sqlで作成済みの'admin'ユーザーを取得
    user2 = db.get_user_by_username('admin')
    assert user2 is not None
    
    # 1. メッセージ作成
    print(f"1. '{user1['username']}' から '{user2['username']}' へメッセージを送信します...")
    db.create_message(user1['id'], user2['id'], "こんにちは、元気ですか")
    print(" -> 成功: メッセージを作成しました。")
    
    # 2. メッセージ取得
    print(f"2. '{user2['username']}' のメッセージボックスを確認します...")
    messages = db.get_messages_for_user(user2['id'])
    assert len(messages) >= 1
    # 最後のメッセージをチェック
    last_message = messages[-1]
    assert last_message['content'] == "こんにちは、元気ですか"
    assert last_message['sender_name'] == user1['username']
    print(" -> 成功: 正しくメッセージが取得できました。")

    print("[テスト完了] メッセージ操作")


def test_transaction_operations(user):
    """決済関連のCRUD操作をテストする"""
    print("\n[テスト開始] 決済操作")
    
    # 1. 決済処理
    print("1. 決済処理を実行します...")
    cart = [
        {'product_id': 1, 'purchase_price': 10.5},
        {'product_id': 2, 'purchase_price': 0.0} # パラメータ改ざんをシミュレート
    ]
    transaction_id = db.create_transaction(user['id'], cart)
    assert transaction_id is not None
    print(f" -> 成功: トランザクションID {transaction_id} が作成されました。")

    # 2. 購入履歴の確認
    print("2. 購入履歴を確認します...")
    history = db.get_purchase_history(user['id'])
    assert len(history) == 2 # 2つの商品アイテム
    
    total_amount_from_history = sum(item['purchase_price'] for item in history)
    assert total_amount_from_history == 10.5 # 0円のアイテムも含まれる
    print(" -> 成功: 購入履歴が正しく記録されています。")
    for item in history:
        print(f"    - 商品: {item['product_name']}, 購入価格: {item['purchase_price']}")

    print("[テスト完了] 決済操作")

def test_session_operations(user):
    """セッション関連のCRUD操作をテストする"""
    print("\n[テスト開始] セッション操作")

    # 1. セッション作成
    print(f"1. ユーザーID {user['id']} のセッションを作成します...")
    session_id = db.create_session(user['id'])
    db.create_session("1")
    assert session_id is not None
    assert isinstance(session_id, str) and len(session_id) == 32
    print(f" -> 成功: セッションID '{session_id}' を作成しました。")

    # 2. セッション取得
    print("2. 作成したセッションIDで情報を取得します...")
    session_data = db.get_session(session_id)
    assert session_data is not None
    assert session_data['user_id'] == user['id']
    print(f" -> 成功: ユーザーID {session_data['user_id']} の有効なセッションが見つかりました。")

    # 3. セッション削除
    print("3. セッションを削除します（ログアウト）...")
    db.delete_session(session_id)
    print(" -> 成功: セッションを削除しました。")

    # 4. 削除後のセッション取得
    print("4. 削除済みのセッションIDで情報を取得します...")
    deleted_session_data = db.get_session(session_id)
    assert deleted_session_data is None
    print(" -> 成功: 削除済みセッションは取得できませんでした。")

    print("[テスト完了] セッション操作")


def print_database_contents():
    """
    データベースの全テーブルの内容を表示する
    """
    print("\n" + "="*50)
    print(" データベースの最終状態を確認します ".center(50, "="))
    print("="*50)

    if not os.path.exists(TEST_DATABASE_FILE):
        print("データベースファイルが見つかりません。")
        return
        
    conn = sqlite3.connect(TEST_DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # テーブル一覧を取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table['name']
        print(f"\n--- テーブル: {table_name} ---")
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            if not rows:
                print("(データなし)")
                continue
            
            # ヘッダーを表示
            headers = rows[0].keys()
            print(" | ".join(f"{h:<20}" for h in headers))
            print("-" * (len(headers) * 23))
            
            # 各行のデータを表示
            for row in rows:
                print(" | ".join(f"{str(v)[:20]:<20}" for v in row))
        except Exception as e:
            print(f"テーブル '{table_name}' の読み込み中にエラー: {e}")
            
    conn.close()


def cleanup():
    """テスト用データベースファイルを削除する"""
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)
        print(f"\n--- テストデータベース '{TEST_DATABASE_FILE}' をクリーンアップしました ---")


if __name__ == '__main__':
    # メインのテスト実行部分
    setup_database()
    
    try:
        # 各テスト関数を実行
        created_user = test_user_operations()
        test_product_operations()
        test_message_operations(created_user)
        test_transaction_operations(created_user)
        test_session_operations(created_user) # セッションテストを追加
        
        print("\n🎉 全てのテストが正常に完了しました。")
        
    except AssertionError as e:
        print(f"\n❌ テスト失敗: {e}")
    except Exception as e:
        print(f"\n❌ 予期せぬエラーが発生しました: {e}")
    finally:
        # テスト完了後、クリーンアップ前にDB内容を表示
        print_database_contents()
        input("\n確認後、Enterキーを押すとクリーンアップして終了します...")
        cleanup()
