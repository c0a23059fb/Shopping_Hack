#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import http.cookies

# utilityディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'utility'))
from database import get_session, get_user_by_id

cgitb.enable()

# セッションチェック
cookie_string = os.environ.get('HTTP_COOKIE', '')
cookies = http.cookies.SimpleCookie()
if cookie_string:
    cookies.load(cookie_string)

session_id = cookies.get('session_id')
current_user = None

if session_id:
    session_id = session_id.value
    # データベースでセッションを確認
    try:
        session = get_session(session_id)
        if session:
            # セッションが有効な場合、ユーザー情報を取得
            user_data = get_user_by_id(session['user_id'])
            if user_data:
                current_user = user_data
            else:
                # ユーザーデータが見つからない場合、ログインページにリダイレクト
                print("Location: index.html")
                print()
                exit()
        else:
            # セッションが無効な場合、ログインページにリダイレクト
            print("Location: index.html")
            print()
            exit()
    except Exception as e:
        # データベースエラーの場合もログインページにリダイレクト
        print("Location: index.html")
        print()
        exit()
else:
    # セッションIDがない場合、ログインページにリダイレクト
    print("Location: index.html")
    print()
    exit()

print("Content-Type: text/html; charset=utf-8")
print()

print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Home</title>
    <style>
        /* CSSスタイルはhome.htmlと同じものをここに貼り付けるか、外部CSSファイルを読み込む */
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
            display: flex;
            flex-direction: column;
            flex-grow: 0;
            margin: auto;
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

        #nav-menu {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            padding: 20px 0;
        }
        .nav-item {
            width: 140px;
            height: 120px;
            border: 2px solid var(--border-color);
            background-color: var(--window-bg);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            text-decoration: none;
            color: var(--text-color);
            box-shadow: 3px 3px 0px rgba(0, 255, 65, 0.3);
            transition: transform 0.1s, box-shadow 0.1s;
        }
        .nav-item:hover {
            transform: translate(2px, 2px);
            box-shadow: 1px 1px 0px rgba(0, 255, 65, 0.3);
            background-color: rgba(0, 255, 65, 0.1);
        }
        .nav-item .icon-placeholder {
            font-size: 3.5em;
            margin-bottom: 5px;
        }
        .nav-item div {
            font-size: 0.9em;
        }
        .nav-item.disabled {
            opacity: var(--disabled-opacity);
            cursor: not-allowed;
            pointer-events: none;
        }
        .nav-item.disabled:hover {
            transform: none;
            box-shadow: 3px 3px 0px rgba(0, 255, 65, 0.3);
            background-color: var(--window-bg);
        }
        .btn { background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 10px 15px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin-right: 10px; }
        .btn:hover:not(:disabled) { background-color: var(--border-color); color: var(--title-bar-text); }
        .btn:disabled { opacity: var(--disabled-opacity); cursor: not-allowed; }

    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar">
            <span>[TERMINAL_X_HOME]</span>
            <form id="logoutForm" method="POST" action="logout.cgi" style="display:inline-block;">
                <button type="submit" class="btn">[logout.sh]</button>
            </form>
        </div>
        <div class="window-content">
            <div id="nav-menu">
                <a href="products.cgi" id="productsLink" class="nav-item">
                    <div class="icon-placeholder">📁</div>
                    <div>[PRODUCTS]</div>
                </a>
                <a href="messenger.cgi" id="messengerLink" class="nav-item">
                    <div class="icon-placeholder">✉</div>
                    <div>[MESSENGER]</div>
                </a>
                <a href="cart.cgi" id="cartLink" class="nav-item">
                    <div class="icon-placeholder">🛒</div>
                    <div>[CART]</div>
                </a>
                <a href="history.cgi" id="historyLink" class="nav-item">
                    <div class="icon-placeholder">🧾</div>
                    <div>[HISTORY]</div>
                </a>
                <a href="help.cgi" id="helpLink" class="nav-item">
                    <div class="icon-placeholder">?</div>
                    <div>[HELP]</div>
                </a>
            </div>
        </div>
    </div>
</body>
</html>
""")