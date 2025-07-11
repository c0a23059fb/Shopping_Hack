#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import cgi
import http.cookies
import utility.database as database

def get_session_id():
    """クッキーまたはURLパラメータからセッションIDを取得"""
    # まずクッキーから取得を試行
    cookies = os.environ.get('HTTP_COOKIE', '')
    if cookies:
        cookie = http.cookies.SimpleCookie(cookies)
        if 'session_id' in cookie:
            return cookie['session_id'].value
    
    # クッキーにない場合はURLパラメータから取得
    form = cgi.FieldStorage()
    if 'session_id' in form:
        return form['session_id'].value
    
    return None

def display_product_card(product):
    """商品情報をカード形式でHTML出力"""
    return f'''
    <div class="product-card">
        <img src="{product['image_url']}" alt="{product['name']}" class="product-image">
        <div class="product-info">
            <h3>{product['name']}</h3>
            <p class="seller">販売者: {product['seller']}</p>
            <p class="price">価格: ${product['price']:.2f}</p>
            <p class="description">{product['description']}</p>
            <button class="add-to-cart" onclick="addToCart({product['id']})">カートに追加</button>
        </div>
    </div>
    '''

def main():
    session_id = get_session_id()
    
    print('Content-Type: text/html; charset=utf-8\r\n')
    
    # セッション確認
    if not session_id or not database.get_session(session_id):
        print('<html><head><title>認証エラー</title></head><body>')
        print('<p>ログインが必要です。</p>')
        print('<a href="/login.cgi">ログイン画面へ</a>')
        print('</body></html>')
        return
    
    # 商品データを取得
    products = database.get_all_products()
    
    # HTML出力開始
    print('''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>商品一覧 - Terminal X</title>
        <style>
            body {
                font-family: 'Courier New', monospace;
                background-color: #0a0a0a;
                color: #00ff41;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            
            .header {
                text-align: center;
                border-bottom: 2px solid #00ff41;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin: 0;
                text-shadow: 0 0 10px #00ff41;
            }
            
            .nav-links {
                margin-top: 15px;
            }
            
            .nav-links a {
                color: #00ff41;
                text-decoration: none;
                margin: 0 15px;
                padding: 5px 10px;
                border: 1px solid #00ff41;
                transition: all 0.3s;
            }
            
            .nav-links a:hover {
                background-color: #00ff41;
                color: #000;
            }
            
            .products-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .product-card {
                background-color: #1a1a1a;
                border: 1px solid #00ff41;
                border-radius: 8px;
                padding: 20px;
                transition: all 0.3s;
            }
            
            .product-card:hover {
                box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
                transform: translateY(-5px);
            }
            
            .product-image {
                width: 100%;
                height: 150px;
                object-fit: cover;
                border-radius: 4px;
                margin-bottom: 15px;
            }
            
            .product-info h3 {
                margin: 0 0 10px 0;
                color: #00ff41;
                font-size: 1.3em;
            }
            
            .seller {
                color: #888;
                margin: 5px 0;
            }
            
            .price {
                color: #ffaa00;
                font-weight: bold;
                font-size: 1.2em;
                margin: 10px 0;
            }
            
            .description {
                color: #ccc;
                margin: 10px 0;
                font-size: 0.9em;
            }
            
            .add-to-cart {
                background-color: transparent;
                border: 1px solid #00ff41;
                color: #00ff41;
                padding: 10px 20px;
                cursor: pointer;
                width: 100%;
                font-family: inherit;
                transition: all 0.3s;
            }
            
            .add-to-cart:hover {
                background-color: #00ff41;
                color: #000;
            }
            
            .no-products {
                text-align: center;
                color: #888;
                font-size: 1.2em;
                margin-top: 50px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>TERMINAL X - 商品一覧</h1>
            <div class="nav-links">
    ''')
    
    print(f'<a href="/index.cgi?session_id={session_id}">ホーム</a>')
    print(f'<a href="/messenger.cgi?session_id={session_id}">メッセージ</a>')
    print(f'<a href="/logout.cgi?session_id={session_id}">ログアウト</a>')
    
    print('''
            </div>
        </div>
        
        <div class="products-grid">
    ''')
    
    # 商品表示
    if products:
        for product in products:
            print(display_product_card(product))
    else:
        print('<div class="no-products">現在、販売中の商品はありません。</div>')
    
    print('''
        </div>
        
        <script>
            function addToCart(productId) {
                // カート機能は将来実装予定
                alert('カート機能は実装中です。商品ID: ' + productId);
            }
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    main()