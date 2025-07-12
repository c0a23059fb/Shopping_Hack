#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import http.cookies
from utility.database import create_transaction, verify_session
import html  # HTMLエスケープ用ライブラリを追加

cgitb.enable()

# セッションチェックの模擬
# バックエンド担当者はここで実際のセッションIDやログイン状態をチェックし、
# ログインしていなければ index.html へリダイレクトするロジックを実装してください。

form = cgi.FieldStorage()
action = form.getvalue('action')

# Cookieからセッション情報を取得
cookie_string = os.environ.get('HTTP_COOKIE', '')
cookies = http.cookies.SimpleCookie()
if cookie_string:
    cookies.load(cookie_string)
# 認証チェック
is_authenticated, user_id = verify_session(cookies)


if not is_authenticated:
    # 認証されていない場合、ログインページにリダイレクト
    print("Location: index.cgi")
    print()
    exit()

if action == 'confirm_purchase':
    try:
        # フォームから送信された商品と価格を取得
        item_ids = form.getlist('item_id')
        item_names = form.getlist('item_name')
        item_prices = form.getlist('item_price')

        cart_items = []
        final_total = 0.0

        for i in range(len(item_ids)):
            try:
                product_id = int(item_ids[i])
                name = item_names[i]
                price = float(item_prices[i])
                cart_items.append({'product_id': product_id, 'purchase_price': price})
                final_total += price
            except (ValueError, TypeError):
                pass

        # 購入履歴をデータベースに保存
        transaction_id = create_transaction(user_id, cart_items)

        print("Content-Type: text/html; charset=utf-8")
        print("Status: 200 OK")  # 正しいステータスコードを追加
        print()
        print(f"""<!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Terminal X - Transaction Result</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=VT323&family=Inconsolata&display=swap');
                :root {{--background-color: #0a0a0a;--text-color: #00ff41;--border-color: #00ff41;--window-bg: #111111;--title-bar-bg: #00ff41;--title-bar-text: #0a0a0a;--disabled-opacity: 0.5;}}
                body {{background-color: var(--background-color);color: var(--text-color);font-family: 'Inconsolata', monospace;overflow: hidden;margin: 0;padding: 0;cursor: default;display: flex;flex-direction: column;align-items: center;justify-content: center;min-height: 100vh;}}
                body::before {{content: '';position: fixed;top: 0;left: 0;width: 100vw;height: 100vh;background-image: linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);background-size: 20px 20px;z-index: -1;}}
                .window-container {{border: 2px solid var(--border-color);background-color: var(--window-bg);box-shadow: 5px 5px 0px rgba(0, 255, 65, 0.3);max-width: 500px;width: 90%;display: flex;flex-direction: column;flex-grow: 0;text-align: center;}}
                .title-bar {{background-color: var(--title-bar-bg);color: var(--title-bar-text);padding: 8px 12px;font-weight: bold;display: flex;justify-content: center;align-items: center;user-select: none;}}
                .window-content {{padding: 15px;flex-grow: 1;}}
                .btn {{background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 10px 15px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin-right: 10px; margin-top: 10px; }}
                .btn:hover:not(:disabled) {{ background-color: var(--border-color); color: var(--title-bar-text); }}
            </style>
            <script>
                sessionStorage.removeItem('shopping_cart_data');
            </script>
        </head>
        <body>
            <div class="window-container">
                <div class="title-bar"><span>[TRANSACTION_COMPLETE]</span></div>
                <div class="window-content">
                    <p>Transaction complete. Total: {final_total:.2f} BTC.</p>
                    <p>Your assets will be delivered shortly.</p>
                    <p><a href="home.cgi" class="btn">[HOME]</a></p>
                </div>
            </div>
        </body>
        </html>""")
    except Exception as e:
        print("Content-Type: text/html; charset=utf-8")
        print("Status: 500 Internal Server Error")
        print()
        print(f"""<!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error</title>
    </head>
    <body>
        <h1>An error occurred</h1>
        <p>{html.escape(str(e))}</p>  <!-- HTMLエスケープを適用 -->
    </body>
    </html>""")
else:
    # カート内容表示
    print("Content-Type: text/html; charset=utf-8")
    print("Status: 200 OK")  # 正しいステータスコードを追加
    print()
    print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Cart</title>
    <style>
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
            max-width: 600px;
            width: 90%;
            height: 90vh;
            display: flex;
            flex-direction: column;
        }

        .title-bar {
            background-color: var(--title-bar-bg);
            color: var(--title-bar-text);
            padding: 8px 12px;
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

        .btn {
            background-color: transparent;
            border: 2px solid var(--border-color);
            color: var(--text-color);
            padding: 10px 15px;
            cursor: pointer;
            font-family: inherit;
            text-transform: uppercase;
            margin-right: 10px;
            margin-top: 10px;
        }

        .btn:hover:not(:disabled) {
            background-color: var(--border-color);
            color: var(--title-bar-text);
        }

        .btn:disabled {
            opacity: var(--disabled-opacity);
            cursor: not-allowed;
        }

        .styled-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .styled-table th, .styled-table td { border: 1px solid var(--border-color); padding: 8px; text-align: left; }
        .styled-table th { background-color: rgba(0, 255, 65, 0.1); }
        .price-input { width: 80px; text-align: right; background-color: #222; border: 1px solid var(--border-color); color: var(--text-color); padding: 5px; font-family: inherit; }
        .price-input:focus { outline: 1px solid var(--text-color); }
        .price-input[readonly] { background-color: #333; }
        .total-row { font-weight: bold; border-top: 2px solid var(--border-color); }

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
            <span>[TRANSACTION_EXECUTION]</span>
            <a href="home.cgi" class="btn">[HOME]</a>
        </div>
        <div class="window-content">
            <form method="POST" action="cart.cgi">
                <input type="hidden" name="action" value="confirm_purchase">
                <table class="styled-table">
                    <thead> <tr> <th>Item Name</th> <th>Price (BTC)</th> </tr> </thead>
                    <tbody id="checkout-items">
                        <!-- Items will be loaded dynamically -->
                    </tbody>
                    <tfoot> <tr class="total-row"> <td>TOTAL:</td> <td id="checkout-total">0.00</td> </tr> </tfoot>
                </table>
                <button type="submit" class="btn" disabled>[CONFIRM & TRANSMIT]</button>
            </form>
        </div>
    </div>

    <div class="common-nav">
        <button class="btn" onclick="window.location.href='products.cgi'">[PRODUCTS]</button>
        <button class="btn" onclick="window.location.href='messenger.cgi'">[MESSENGER]</button>
        <button class="btn" onclick="window.location.href='cart.cgi'">[CART]</button>
        <button class="btn" onclick="window.location.href='history.cgi'">[HISTORY]</button>
        <button class="btn" onclick="window.location.href='help.cgi'">[HELP]</button>
    </div>

    <script>
        // sessionStorageからカートデータを取得してページに表示
        window.onload = function() {
            const cartData = JSON.parse(sessionStorage.getItem('shopping_cart_data')) || [];
            const checkoutItems = document.getElementById('checkout-items');
            const checkoutTotal = document.getElementById('checkout-total');
            const confirmButton = document.querySelector('button[type="submit"]');
            
            if (cartData.length === 0) {
                checkoutItems.innerHTML = '<tr><td colspan="2">Shopping cart is empty.</td></tr>';
                checkoutTotal.textContent = '0.00';
                confirmButton.disabled = true;
            } else {
                let totalPrice = 0;
                checkoutItems.innerHTML = '';
                
                cartData.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = 
                        '<td>' + item.name + '</td>' +
                        '<td>' +
                            '<input type="text" class="price-input" name="item_price" value="' + item.price.toFixed(2) + '" readonly>' +
                            '<input type="hidden" name="item_name" value="' + item.name + '">' +
                            '<input type="hidden" name="item_id" value="' + item.id + '">' +
                        '</td>';
                    checkoutItems.appendChild(row);
                    totalPrice += item.price;
                });
                
                checkoutTotal.textContent = totalPrice.toFixed(2);
                confirmButton.disabled = false;
            }
        };
    </script>
</body>
</html>""")