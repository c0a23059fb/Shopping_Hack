#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import http.cookies
import cgitb
from datetime import datetime
from utility.database import verify_session, get_purchase_history

cgitb.enable()

# セッションチェック
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


# ログインしているユーザーの購入履歴を取得
purchase_history = get_purchase_history(user_id)

print("Content-Type: text/html; charset=utf-8")
print()

print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - History</title>
    <style>
        /* CSSスタイルはhistory.htmlと同じものをここに貼り付けるか、外部CSSファイルを読み込む */
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
            max-width: 800px;
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

        #history-log { background-color: #000; border: 1px solid var(--border-color); padding: 10px; white-space: pre-wrap; overflow-x: auto; text-align: left; flex-grow: 1; font-size: 0.9em;}

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
            background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 8px 12px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin: 0; font-size: 0.9em;
        }
        .btn:hover { background-color: var(--border-color); color: var(--title-bar-text); }
    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar">
            <span>[ORDER_HISTORY.LOG]</span>
            <a href="home.cgi" class="btn">[HOME]</a>
        </div>
        <div class="window-content">
            <div id="history-log">
""")

if not purchase_history:
    print('No order history found.')
else:
    for record in purchase_history:
        # 日付をYYYY-MM-DD HH:MM:SS形式に変換
        formatted_date = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        print(f'ACTION:PURCHASE | DATE:{formatted_date} | TOTAL:{record["total_amount"]:.2f} BTC')
        print(f'  - ITEM: {record["product_name"]} | PRICE: {record["purchase_price"]:.2f}')
        print('-----------------------------------------------------')

print("""            </div>
        </div>
    </div>

    <div class="common-nav">
        <button class="btn" onclick="window.location.href='products.cgi'">[PRODUCTS]</button>
        <button class="btn" onclick="window.location.href='messenger.cgi'">[MESSENGER]</button>
        <button class="btn" onclick="window.location.href='cart.cgi'">[CART]</button>
        <button class="btn" onclick="window.location.href='history.cgi'">[HISTORY]</button>
        <button class="btn" onclick="window.location.href='help.cgi'">[HELP]</button>
    </div>
</body>
</html>
""")