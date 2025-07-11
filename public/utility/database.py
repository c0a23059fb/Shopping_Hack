import mysql.connector
from mysql.connector import Error
import crypt
import os
import string
from datetime import datetime, timedelta

# MySQL接続設定
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passwordA1!',
    'database': 'terminal_x'
}

def get_db_connection():
    """データベース接続を取得し、辞書形式で結果を返せるように設定"""
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        return conn
    except Error as e:
        print(f"MySQL接続エラー: {e}")
        raise

# --- User CRUD ---

def create_user(username, password):
    """
    新規ユーザーを作成する。cryptライブラリとランダムなソルトを使用。
    """
    salt = '$6$' + ''.join(os.urandom(8).hex())
    password_crypt = crypt.crypt(password, salt)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_crypt)
        )
        conn.commit()
    except mysql.connector.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
        return None
    finally:
        conn.close()
        
    return get_user_by_username(username)

def get_user_by_username(username):
    """ユーザー名でユーザー情報を取得する。"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """ユーザーIDでユーザー情報を取得する。"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_password(username, password):
    """
    ユーザー名とパスワードを検証する。
    """
    user = get_user_by_username(username)
    if not user:
        return False
    
    return crypt.crypt(password, user['password_hash']) == user['password_hash']


# --- Session CRUD (新規追加) ---

def create_session(user_id):
    """
    指定されたユーザーIDのセッションを作成し、セッションIDを返す。
    セッションの有効期限は1時間とする。
    """
    session_id = os.urandom(16).hex() # 32文字のランダムなセッションID
    expires_at = datetime.now() + timedelta(hours=1)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_id, user_id, expires_at) VALUES (%s, %s, %s)",
        (session_id, user_id, expires_at)
    )
    conn.commit()
    conn.close()
    
    return session_id

def get_session(session_id):
    """
    セッションIDでセッション情報を取得する。
    有効期限が切れていないセッションのみを返す。
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM sessions WHERE session_id = %s AND expires_at > %s",
        (session_id, datetime.now())
    )
    session = cursor.fetchone()
    conn.close()
    return session

def delete_session(session_id):
    """
    セッションIDでセッションを削除する（ログアウト処理）。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = %s", (session_id,))
    conn.commit()
    conn.close()

def delete_user_sessions(user_id):
    """
    指定されたユーザーIDの全セッションを削除する。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()


# --- Product CRUD (変更なし) ---

def get_all_products():
    """すべての商品情報を取得する。"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id")
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    """商品IDで単一の商品情報を取得する。"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

# --- Message CRUD (変更なし) ---

def create_message(sender_id, recipient_id, content):
    """新規メッセージを作成する。"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_id, recipient_id, content) VALUES (%s, %s, %s)",
        (sender_id, recipient_id, content)
    )
    conn.commit()
    conn.close()

def get_messages_for_user(user_id):
    """特定のユーザーが送受信した全メッセージを取得する。"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT m.*, s.username as sender_name, r.username as recipient_name FROM messages m "
        "JOIN users s ON m.sender_id = s.id "
        "JOIN users r ON m.recipient_id = r.id "
        "WHERE m.sender_id = %s OR m.recipient_id = %s ORDER BY m.sent_at ASC",
        (user_id, user_id)
    )
    messages = cursor.fetchall()
    conn.close()
    return messages
    
# --- Transaction CRUD (変更なし) ---

def create_transaction(user_id, cart_items):
    """
    決済処理を行い、トランザクションと詳細レコードを作成する。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        total_amount = sum(item['purchase_price'] for item in cart_items)
        cursor.execute(
            "INSERT INTO transactions (user_id, total_amount) VALUES (%s, %s)",
            (user_id, total_amount)
        )
        transaction_id = cursor.lastrowid
        for item in cart_items:
            cursor.execute(
                "INSERT INTO transaction_items (transaction_id, product_id, purchase_price) VALUES (%s, %s, %s)",
                (transaction_id, item['product_id'], item['purchase_price'])
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()
    
    return transaction_id

def get_purchase_history(user_id):
    """特定のユーザーの全購入履歴を取得する。"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT t.id as transaction_id, t.total_amount, t.created_at, ti.purchase_price, p.name as product_name "
        "FROM transactions t "
        "JOIN transaction_items ti ON t.id = ti.transaction_id "
        "JOIN products p ON ti.product_id = p.id "
        "WHERE t.user_id = %s ORDER BY t.created_at DESC",
        (user_id,)
    )
    history = cursor.fetchall()
    conn.close()
    return history
