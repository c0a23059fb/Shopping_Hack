#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import http.cookies

# utilityディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'utility'))
from database import delete_session

# エラー発生時に詳細なトレースバックを表示（開発用）
cgitb.enable()

# Cookieからセッション情報を取得
cookie_string = os.environ.get('HTTP_COOKIE', '')
cookies = http.cookies.SimpleCookie()
if cookie_string:
    cookies.load(cookie_string)

session_id = cookies.get('session_id')
if session_id:
    session_id = session_id.value

# HTTPヘッダーを出力（Cookieを削除）
print("Content-Type: text/html; charset=utf-8")
if session_id:
    # セッションをデータベースから削除
    try:
        delete_session(session_id)
    except Exception as e:
        print(f"<!-- Session deletion error: {str(e)} -->")
    
    # Cookieを削除
    print("Set-Cookie: session_id=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/")

print() # ヘッダーと本文の間の空行

# 以下、HTMLコンテンツ
print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Logout</title>
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
            max-width: 500px;
            width: 90%;
            display: flex;
            flex-direction: column;
            flex-grow: 0;
        }

        .title-bar {
            background-color: var(--title-bar-bg);
            color: var(--title-bar-text);
            padding: 8px 12px;
            font-weight: bold;
            display: flex;
            justify-content: center;
            align-items: center;
            user-select: none;
        }

        .window-content {
            padding: 15px;
            overflow-y: auto;
            flex-grow: 1;
        }

    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar"> <span>[LOGOUT_RESULT]</span> </div>
        <div class="window-content">
            <p>Logout successful. Session has been terminated.</p>
            <p>Redirecting to login page...</p>
            <meta http-equiv="refresh" content="2;url=index.html">
        </div>
    </div>
</body>
</html>
""")
