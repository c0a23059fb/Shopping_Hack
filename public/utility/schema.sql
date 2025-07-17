-- データベースの初期化とテーブル作成用SQL (MySQL用)

-- データベースの作成と使用
CREATE DATABASE IF NOT EXISTS terminal_x;
USE terminal_x;

-- 古いテーブルが存在すれば削除 (依存関係の逆順で削除)
DROP TABLE IF EXISTS transaction_items;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- ユーザーテーブル
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 商品テーブル
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    seller VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    image_url TEXT,
    description TEXT
);

-- セッション管理テーブル
CREATE TABLE sessions (
    session_id VARCHAR(64) PRIMARY KEY NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (username) ON DELETE CASCADE
);

-- メッセージテーブル
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (recipient_id) REFERENCES users (id)
);

-- トランザクション（決済）テーブル
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- トランザクション詳細テーブル
CREATE TABLE transaction_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    product_id INT NOT NULL,
    purchase_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (transaction_id) REFERENCES transactions (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- 初期データの投入
INSERT INTO users (username, password_hash) VALUES
('admin','$6$5c814a18248db4bf$tZDj62FpcX1ih2zQY4wvZvSrs0DlW8AU1AE9rQghdxAcspsTNDTCHF8h6FeI/LPNF5Cc1xkJfCi.fi6eJfiA7/'),
('user1','$6$dd537d8a48d14e5a$NyGpe5348Msu4QJ9oIdI2DwrVmyVKhQt3nE0lsBlYF9/Hgu1MrGFuq/bQX97rr1UL0DD9zApwI.Ffa7XLgqke0');

INSERT INTO products (name, seller, price, image_url, description) VALUES
('USB', 'Vendor_A5', 0.05, 'images/products/USBmemory.png', 'hacking用usbメモリ'),
('スマホ', 'CipherMaster', 5.00, 'images/products/smartphone.png', '飛ばし用スマホ'),
('薬', 'ShadowCorp', 3.50, 'images/products/drugtwo.png', '見てわかる'),
('葉っぱ', 'GhostSec', 50.00, 'images/products/malifana.png', '吸うのにいい。');