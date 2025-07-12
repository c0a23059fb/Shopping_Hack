## **データベース設計書 (MySQL)**

アプリケーション全体で使用するデータベースの構造を定義します。

| No. | テーブル名（論理名） | テーブル名（物理名） | 説明                                                       |
| :-- | :------------------- | :------------------- | :--------------------------------------------------------- |
| 1   | ユーザー             | users                | ログインするユーザーの情報を格納する。                     |
| 2   | 商品                 | products             | 販売する商品の情報を格納する。                             |
| 3   | セッション           | sessions             | ユーザーのログイン状態を管理する。                         |
| 4   | トランザクション     | transactions         | ユーザーの購入単位（決済）の情報を格納する。               |
| 5   | トランザクション詳細 | transaction_items    | 1 回のトランザクションに含まれる個々の商品情報を格納する。 |
| 6   | メッセージ           | messages             | ユーザー間のダイレクトメッセージを格納する。               |

### **1\. ユーザーテーブル (users)**

| カラム名（論理名） | カラム名（物理名） | データ型       | 制約                      | 説明                       |
| :----------------- | :----------------- | :------------- | :------------------------ | :------------------------- |
| ユーザー ID        | id                 | INT            | PRIMARY KEY AUTO_INCREMENT | 一意のユーザー識別子       |
| ユーザー名         | username           | VARCHAR(255)   | NOT NULL UNIQUE           | ログインに使用する名前     |
| パスワードハッシュ | password_hash      | VARCHAR(255)   | NOT NULL                  | ハッシュ化されたパスワード |
| 作成日時           | created_at         | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP | ユーザー作成日時           |

### **2\. 商品テーブル (products)**

| カラム名（論理名） | カラム名（物理名） | データ型       | 制約                      | 説明                     |
| :----------------- | :----------------- | :------------- | :------------------------ | :----------------------- |
| 商品 ID            | id                 | INT            | PRIMARY KEY AUTO_INCREMENT | 一意の商品識別子         |
| 商品名             | name               | VARCHAR(255)   | NOT NULL                  | 商品の名前               |
| 販売者             | seller             | VARCHAR(255)   |                           | 販売者の名前             |
| 価格               | price              | DECIMAL(10,2)  | NOT NULL                  | 商品の価格 (BTC)         |
| 画像 URL           | image_url          | TEXT           |                           | 商品画像のパスまたは URL |
| 説明               | description        | TEXT           |                           | 商品の詳細な説明         |

### **3\. セッションテーブル (sessions)**

| カラム名（論理名） | カラム名（物理名） | データ型       | 制約                            | 説明                         |
| :----------------- | :----------------- | :------------- | :------------------------------ | :--------------------------- |
| セッション ID      | session_id         | VARCHAR(64)    | PRIMARY KEY NOT NULL            | 一意のセッション識別子       |
| ユーザー ID        | user_id            | INT            | NOT NULL, FOREIGN KEY(users.id) | セッションの所有者のユーザーID |
| 作成日時           | created_at         | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP       | セッション作成日時           |
| 有効期限           | expires_at         | TIMESTAMP      | NOT NULL                        | セッションの有効期限         |

### **4\. トランザクションテーブル (transactions)**

| カラム名（論理名）  | カラム名（物理名） | データ型       | 制約                            | 説明                  |
| :------------------ | :----------------- | :------------- | :------------------------------ | :-------------------- |
| トランザクション ID | id                 | INT            | PRIMARY KEY AUTO_INCREMENT       | 一意の取引識別子      |
| ユーザー ID         | user_id            | INT            | NOT NULL, FOREIGN KEY(users.id) | 購入したユーザーの ID |
| 合計金額            | total_amount       | DECIMAL(10,2)  | NOT NULL                        | 取引の合計金額        |
| 取引日時            | created_at         | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP       | 取引が実行された日時  |

### **5\. トランザクション詳細テーブル (transaction_items)**

| カラム名（論理名）  | カラム名（物理名） | データ型       | 制約                                   | 説明                           |
| :------------------ | :----------------- | :------------- | :------------------------------------- | :----------------------------- |
| 詳細 ID             | id                 | INT            | PRIMARY KEY AUTO_INCREMENT              | 一意の取引詳細識別子           |
| トランザクション ID | transaction_id     | INT            | NOT NULL, FOREIGN KEY(transactions.id) | どの取引に属するかを示す ID    |
| 商品 ID             | product_id         | INT            | NOT NULL, FOREIGN KEY(products.id)     | 購入された商品の ID            |
| 購入時価格          | purchase_price     | DECIMAL(10,2)  | NOT NULL                               | 購入が確定した時点での商品価格 |
| 数量                | quantity           | INT            | NOT NULL DEFAULT 1                     | 購入数量                       |

### **6\. メッセージテーブル (messages)**

| カラム名（論理名） | カラム名（物理名） | データ型       | 制約                            | 説明                              |
| :----------------- | :----------------- | :------------- | :------------------------------ | :-------------------------------- |
| メッセージ ID      | id                 | INT            | PRIMARY KEY AUTO_INCREMENT       | 一意のメッセージ識別子            |
| 送信者 ID          | sender_id          | INT            | NOT NULL, FOREIGN KEY(users.id) | メッセージを送信したユーザーの ID |
| 受信者 ID          | recipient_id       | INT            | NOT NULL, FOREIGN KEY(users.id) | メッセージを受信したユーザーの ID |
| 本文               | content            | TEXT           | NOT NULL                        | メッセージの内容                  |
| 送信日時           | sent_at            | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP       | メッセージの送