-- データベースの初期化とテーブル作成用SQL

-- 古いテーブルが存在すれば削除 (依存関係の逆順で削除)
DROP TABLE IF EXISTS transaction_items;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS sessions; -- sessionsテーブルを削除
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- ユーザーテーブル
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 商品テーブル
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    seller TEXT,
    price REAL NOT NULL,
    image_url TEXT,
    description TEXT
);

-- セッション管理テーブル (新規追加)
-- ログイン状態を管理する
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE -- ユーザーが削除されたらセッションも削除
);

-- メッセージテーブル
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (recipient_id) REFERENCES users (id)
);

-- トランザクション（決済）テーブル
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- トランザクション詳細テーブル
CREATE TABLE transaction_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    purchase_price REAL NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (transaction_id) REFERENCES transactions (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- 初期データの投入（例）
INSERT INTO users (username, password_hash) VALUES
('admin','$6$b885fd49ac4f99b3$'),
('user1','$6$b64cd10bb09df0a0$');

INSERT INTO products (name, seller, price, image_url, description) VALUES
('Item_X123', 'Vendor_A5', 0.05, 'https://placehold.co/64x64/000000/00ff41?text=X123', 'A versatile toolkit for network reconnaissance.'),
('Cipher_003', 'CipherMaster', 5.00, 'https://placehold.co/64x64/000000/00ff41?text=C003', 'Military-grade encryption/decryption suite.'),
('Enigma_Pack', 'ShadowCorp', 3.50, 'https://placehold.co/64x64/000000/00ff41?text=ENIG', 'A pack of social engineering templates.'),
('ZeroDay_Exploit', 'GhostSec', 50.00, 'https://placehold.co/64x64/000000/00ff41?text=0DAY', 'Undisclosed exploit for a popular OS.');