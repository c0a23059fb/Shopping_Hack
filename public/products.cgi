#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import http.cookies
from utility.database import get_all_products,verify_session

cgitb.enable()

# セッションチェックの模擬
# バックエンド担当者はここで実際のセッションIDやログイン状態をチェックし、
# ログインしていなければ index.html へリダイレクトするロジックを実装してください。
# 例: if not is_logged_in(): print("Location: index.html\n"); exit()
# セッションチェックと認証チェック
cookie_string = os.environ.get('HTTP_COOKIE', '')
cookies = http.cookies.SimpleCookie()
if cookie_string:
    cookies.load(cookie_string)
# 認証チェック
is_authenticated, current_user = verify_session(cookies)


if not is_authenticated:
    # 認証されていない場合、ログインページにリダイレクト
    print("Location: index.cgi")
    print()
    exit()

    
form = cgi.FieldStorage()
product_id = form.getvalue('product_id')  # 商品詳細表示のためのID
search_query = form.getvalue('search_query')  # 検索キーワード

# 商品データをデータベースから取得
products_data = get_all_products()

print("Content-Type: text/html; charset=utf-8")
print()

print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Products</title>
    <style>
        /* CSSスタイルはproducts.htmlと同じものをここに貼り付けるか、外部CSSファイルを読み込む */
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Inconsolata&display=swap');
        :root {
            --background-color: #0a0a0a;
            --text-color: #00ff41;
            --border-color: #00ff41;
            --window-bg: #111111;
            --title-bar-bg: #00ff41;
            --title-bar-text: #0a0a0a;
            --disabled-opacity: 0.5;
        }
        body {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Inconsolata', monospace;
            overflow: hidden;
            margin: 0;
            padding: 0;
            cursor: default;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image:
                linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            z-index: -1;
        }

        .window-container {
            border: 2px solid var(--border-color);
            background-color: var(--window-bg);
            box-shadow: 5px 5px 0px rgba(0, 255, 65, 0.3);
            max-width: 900px;
            width: 90%;
            # height: 90vh;
            display: flex;
            flex-direction: column;
        }

        .title-bar {
            # background-color: var(--title-bar-bg);
            # color: var(--title-bar-text);
            # padding: 8px 12px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }

        .window-content {
            padding: 15px;
            overflow-y: auto;
            flex-grow: 1;
        }

        .form-group { margin-bottom: 15px; text-align: left; }
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input, .form-group textarea { background-color: #222; border: 1px solid var(--border-color); color: var(--text-color); padding: 6px; width: calc(100% - 20px); font-family: inherit; }
        .form-group input:focus, .form-group textarea:focus { outline: 1px solid var(--text-color); }
        .btn { background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 10px 15px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin-right: 10px; margin-top: 10px; }
        .btn:hover:not(:disabled) { background-color: var(--border-color); color: var(--title-bar-text); }
        .btn:disabled { opacity: var(--disabled-opacity); cursor: not-allowed; }

        .styled-table { width: 100%; border-collapse: collapse; }
        .styled-table th, .styled-table td { border: 1px solid var(--border-color); padding: 6px; text-align: left; }
        .styled-table th { background-color: rgba(0, 255, 65, 0.1); }
        .styled-table tbody tr.clickable { cursor: pointer; }
        .styled-table tbody tr.clickable:hover { background-color: rgba(0, 255, 65, 0.2); }
        .product-thumbnail { width: 40px; height: 40px; object-fit: cover; background-color: #333; border: 1px solid var(--border-color); }

        .detail-layout { display: flex; gap: 20px; }
        .detail-image-container { flex: 1; text-align: center; }
        .detail-image { max-width: 150px; border: 2px solid var(--border-color); background-color: #222; padding: 5px; }
        .detail-info { flex: 2; }
        .reviews-section { margin-top: 20px; border-top: 1px solid var(--border-color); padding-top: 10px; }
        .reviews-section h4 { margin-top: 0; }

        .common-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: var(--window-bg);
            border-top: 2px solid var(--border-color);
            padding: 5px 10px;
            display: flex;
            justify-content: center;
            gap: 15px;
            z-index: 9999;
        }
        .common-nav .btn {
            margin: 0;
            padding: 8px 12px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar">
""")

if product_id:
    # 商品詳細表示
    product = next((p for p in products_data if p['id'] == int(product_id)), None)
    if product:
        print(f"            <span>[ITEM_DETAILS]</span>")
        print(f'            <div style="display: flex; gap: 10px;">')
        print(f'                <form method="GET" action="products.cgi" style="display:inline-block;">')
        print(f'                    <button type="submit" class="btn">[BACK]</button>')
        print(f'                </form>')
        print(f'                <button class="btn" onclick="addSingleToCart({product['id']}, \'{product['name']}\', {product['price']})">[ADD TO CART]</button>')
        print(f'            </div>')
    else:
        print(f"            <span>[PRODUCT_CATALOG]</span>") # エラー時は一覧に戻す
elif form.getvalue('action') == 'add_to_cart':
    print(f"            <span>[PRODUCT_CATALOG]</span>") # カート追加後の表示
    print(f'            <button class="btn" onclick="addSelectedToCart()" style="margin-left: 10px;">[ADD SELECTED TO CART]</button>')
else:
    print(f"            <span>[PRODUCT_CATALOG]</span>")
    print(f'            <button class="btn" onclick="addSelectedToCart()" style="margin-left: 10px;">[ADD SELECTED TO CART]</button>')

print(f'            <a href="home.cgi" class="btn">[HOME]</a>')
print(f"""        </div>
        <div class="window-content">
            <form method="GET" action="products.cgi" style="margin-bottom: 20px;">
                <input type="text" name="search_query" placeholder="Search products..." value="" style="width: calc(100% - 20px); padding: 8px; border: 1px solid var(--border-color); background-color: #222; color: var(--text-color);">
                <button type="submit" class="btn">[SEARCH]</button>
            </form>
""")

if search_query:
    # 検索結果表示
    print("""            <table class="styled-table">
                <thead> <tr> <th>Select</th> <th>IMG</th> <th>ID</th> <th>ITEM_NAME</th> <th>SELLER</th> <th>PRICE (BTC)</th> </tr> </thead>
                <tbody>""")
    for p in products_data:
        if search_query.lower() in p['name'].lower() or search_query.lower() in p['description'].lower():
            print(f'                    <tr data-id="{p["id"]}" data-name="{p["name"]}" data-price="{p["price"]}">')
            print(f'                        <td><input type="checkbox" class="product-checkbox"></td>')
            print(f'                        <td><img src="{p["image_url"]}" alt="{p["name"]}" class="product-thumbnail" onerror="this.onerror=null; this.src=\'https://placehold.co/64x64/000000/00ff41?text=ERR\';"></td>')
            print(f'                        <td>{p["id"]}</td>')
            print(f'                        <td><a href="products.cgi?product_id={p["id"]}" style="color:var(--text-color); text-decoration:none;">{p["name"]}</a></td>')
            print(f'                        <td>{p["seller"]}</td>')
            print(f'                        <td>{p["price"]:.2f}</td>')
            print(f'                    </tr>')
    print("""                </tbody>
            </table>
""")
elif product_id and product:
    print(f"""            <div class="detail-layout">
                <div class="detail-image-container"> <img id="detail-img" src="{product['image'].replace('64x64', '150x150')}" alt="Product Image" class="detail-image" onerror="this.onerror=null; this.src='https://placehold.co/150x150/000000/00ff41?text=NO_IMG';"> </div>
                <div class="detail-info">
                    <div class="form-group"> <label>Item Name</label> <input type="text" id="detail-name" value="{product['name']}" readonly> </div>
                    <div class="form-group"> <label>Price (BTC)</label> <input type="text" id="detail-price" value="{product['price']:.2f}" readonly> </div>
                    <div class="form-group"> <label>Description</label> <textarea id="detail-desc" rows="4" readonly>{product['description']}</textarea> </div>
                </div>
            </div>
            <div class="reviews-section">
                <button class="btn" onclick="addSingleToCart({product['id']}, '{product['name']}', {product['price']})">[ADD TO CART]</button>
            </div>
""")
elif form.getvalue('action') == 'add_to_cart':
    # カート追加処理のメッセージ表示 (実際はcart.cgiで処理されるべきだが、ここでは確認用)
    add_product_id = form.getvalue('product_id')
    added_product = next((p for p in products_data if p['id'] == int(add_product_id)), None)
    if added_product:
        print(f"<p>Added '{added_product['name']}' to cart.</p>")
        print("<p>Please return to the product list.</p>")
    else:
        print("<p>Error adding item to cart.</p>")
    # カート追加後も商品リストを表示
    print("""            <table class="styled-table">
                <thead> <tr> <th>Select</th> <th>IMG</th> <th>ID</th> <th>ITEM_NAME</th> <th>SELLER</th> <th>PRICE (BTC)</th> </tr> </thead>
                <tbody>""")
    for p in products_data:
        print(f'                    <tr data-id="{p["id"]}" data-name="{p["name"]}" data-price="{p["price"]}">')
        print(f'                        <td><input type="checkbox" class="product-checkbox"></td>')
        print(f'                        <td><img src="{p["image_url"]}" alt="{p["name"]}" class="product-thumbnail" onerror="this.onerror=null; this.src=\'https://placehold.co/64x64/000000/00ff41?text=ERR\';"></td>')
        print(f'                        <td>{p["id"]}</td>')
        print(f'                        <td><a href="products.cgi?product_id={p["id"]}" style="color:var(--text-color); text-decoration:none;">{p["name"]}</a></td>')
        print(f'                        <td>{p["seller"]}</td>')
        print(f'                        <td>{p["price"]:.2f}</td>')
        print(f'                    </tr>')
    print("""                </tbody>
            </table>
""")
else:
    # 商品一覧表示
    print("""            <table class="styled-table">
                <thead> <tr> <th>Select</th> <th>IMG</th> <th>ID</th> <th>ITEM_NAME</th> <th>SELLER</th> <th>PRICE (BTC)</th> </tr> </thead>
                <tbody>""")
    for p in products_data:
        print(f'                    <tr data-id="{p["id"]}" data-name="{p["name"]}" data-price="{p["price"]}">')
        print(f'                        <td><input type="checkbox" class="product-checkbox"></td>')
        print(f'                        <td><img src="{p["image_url"]}" alt="{p["name"]}" class="product-thumbnail" onerror="this.onerror=null; this.src=\'https://placehold.co/64x64/000000/00ff41?text=ERR\';"></td>')
        print(f'                        <td>{p["id"]}</td>')
        print(f'                        <td><a href="products.cgi?product_id={p["id"]}" style="color:var(--text-color); text-decoration:none;">{p["name"]}</a></td>')
        print(f'                        <td>{p["seller"]}</td>')
        print(f'                        <td>{p["price"]:.2f}</td>')
        print(f'                    </tr>')
    print("""                </tbody>
            </table>
""")

print("""        </div>
    </div>

    <div class="common-nav">
        <button class="btn" onclick="window.location.href='products.cgi'">[PRODUCTS]</button>
        <button class="btn" onclick="window.location.href='messenger.cgi'">[MESSENGER]</button>
        <button class="btn" onclick="window.location.href='cart.cgi'">[CART]</button>
        <button class="btn" onclick="window.location.href='history.cgi'">[HISTORY]</button>
        <button class="btn" onclick="window.location.href='help.cgi'">[HELP]</button>
    </div>

    <script>
        function addSelectedToCart() {
            const selectedProducts = [];
            document.querySelectorAll('.product-checkbox:checked').forEach(checkbox => {
                const row = checkbox.closest('tr');
                const productId = parseInt(row.dataset.id);
                const productName = row.dataset.name;
                const productPrice = parseFloat(row.dataset.price);

                selectedProducts.push({ id: productId, name: productName, price: productPrice });
            });

            if (selectedProducts.length === 0) {
                alert('Please select at least one product.');
                return;
            }

            // 既存のカートデータを取得
            const existingCart = JSON.parse(sessionStorage.getItem('shopping_cart_data')) || [];
            
            // 重複チェックと新規商品の追加
            selectedProducts.forEach(newProduct => {
                const existingIndex = existingCart.findIndex(item => item.id === newProduct.id);
                if (existingIndex === -1) {
                    existingCart.push(newProduct);
                }
            });

            sessionStorage.setItem('shopping_cart_data', JSON.stringify(existingCart));
            alert(`${selectedProducts.length} item(s) added to cart!`);
            
            // チェックボックスをリセット
            document.querySelectorAll('.product-checkbox').forEach(checkbox => {
                checkbox.checked = false;
            });
        }

        function addSingleToCart(id, name, price) {
            // 既存のカートデータを取得
            const existingCart = JSON.parse(sessionStorage.getItem('shopping_cart_data')) || [];
            
            // 重複チェック
            const existingIndex = existingCart.findIndex(item => item.id === id);
            if (existingIndex === -1) {
                existingCart.push({ id: id, name: name, price: price });
                sessionStorage.setItem('shopping_cart_data', JSON.stringify(existingCart));
                alert(`${name} added to cart!`);
            } else {
                alert(`${name} is already in your cart.`);
            }
        }
    </script>
</body>
</html>
""")