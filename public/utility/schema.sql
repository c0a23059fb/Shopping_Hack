-- データベースの初期化とテーブル作成用SQL (MySQL用)

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
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
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
('admin','$6$8a5cb7be35313ee1$0swEW0uf6Y8OTjTN7cHaWA2MpHmuF5YeFtNz32AxEXqLi9CNObYESfla9xnhULKhdLfK1pwCKQmeGL2hLfPjx'),
('user1','$6$dd537d8a48d14e5a$NyGpe5348Msu4QJ9oIdI2DwrVmyVKhQt3nE0lsBlYF9/Hgu1MrGFuq/bQX97rr1UL0DD9zApwI.Ffa7XLgqke0');

INSERT INTO products (name, seller, price, image_url, description) VALUES
('Item_X123', 'Vendor_A5', 0.05, 'https://placehold.co/64x64/000000/00ff41?text=X123', 'A versatile toolkit for network reconnaissance.'),
('Cipher_003', 'CipherMaster', 5.00, 'https://placehold.co/64x64/000000/00ff41?text=C003', 'Military-grade encryption/decryption suite.'),
('Enigma_Pack', 'ShadowCorp', 3.50, 'https://placehold.co/64x64/000000/00ff41?text=ENIG', 'A pack of social engineering templates.'),
('ZeroDay_Exploit', 'GhostSec', 50.00, 'https://placehold.co/64x64/000000/00ff41?text=0DAY', 'Undisclosed exploit for a popular OS.')