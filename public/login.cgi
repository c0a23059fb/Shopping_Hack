#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import http.cookies
from datetime import datetime, timedelta

# utilityディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'utility'))
from database import create_user, verify_password, get_user_by_username, create_session, delete_user_sessions

# エラー発生時に詳細なトレースバックを表示（開発用）
cgitb.enable()

def print_html_header():
    """HTML開始部分を出力する関数"""
    print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Login Process</title>
    <style>
        /* CSSスタイルはindex.htmlと同じものをここに貼り付けるか、外部CSSファイルを読み込む */
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
        
        .btn { background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 10px 15px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin-right: 10px; margin-top: 10px; }
        .btn:hover:not(:disabled) { background-color: var(--border-color); color: var(--title-bar-text); }
        .btn:disabled { opacity: var(--disabled-opacity); cursor: not-allowed; }

    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar"> <span>[AUTHENTICATION_RESULT]</span> </div>
        <div class="window-content">
""")

def print_html_footer():
    """HTML終了部分を出力する関数"""
    print("""
        </div>
    </div>
</body>
</html>
""")

# フォームデータを取得
form = cgi.FieldStorage()

action = form.getvalue('action')
username = form.getvalue('username')
password = form.getvalue('password')

# データベースを使用した認証処理
try:
    if action == 'login':
        if username and password:
            # データベースでユーザー認証
            if verify_password(username, password):
                user = get_user_by_username(username)
                # 既存のセッションを削除してから新しいセッションを作成
                delete_user_sessions(user['id'])
                session_id = create_session(user['id'])
                
                # HTTPヘッダーを出力（Cookieを含む）
                print("Content-Type: text/html; charset=utf-8")
                print(f"Set-Cookie: session_id={session_id}; HttpOnly; Path=/")
                print() # ヘッダーと本文の間の空行
                
                # 成功ページを表示
                print_html_header()
                print(f"<p>Login successful for user: {username}</p>")
                print('<p>Redirecting to home...</p>')
                print('<meta http-equiv="refresh" content="2;url=home.cgi">')
                print_html_footer()
            else:
                # HTTPヘッダーを出力
                print("Content-Type: text/html; charset=utf-8")
                print() # ヘッダーと本文の間の空行
                
                print_html_header()
                print("<p>Login failed: Invalid username or password.</p>")
                print('<p>Redirecting back to login...</p>')
                print('<meta http-equiv="refresh" content="2;url=index.html">')
                print_html_footer()
        else:
            # HTTPヘッダーを出力
            print("Content-Type: text/html; charset=utf-8")
            print() # ヘッダーと本文の間の空行
            
            print_html_header()
            print("<p>Error: Username and password are required.</p>")
            print('<p>Redirecting back to login...</p>')
            print('<meta http-equiv="refresh" content="2;url=index.html">')
            print_html_footer()
            
    elif action == 'create_user':
        # HTTPヘッダーを出力
        print("Content-Type: text/html; charset=utf-8")
        print() # ヘッダーと本文の間の空行
        
        print_html_header()
        if username and password:
            try:
                # データベースに新規ユーザーを作成
                new_user = create_user(username, password)
                if new_user:
                    print(f"<p>User '{username}' created successfully!</p>")
                    print('<p>You can now log in with your credentials.</p>')
                    print('<p>Redirecting back to login...</p>')
                    print('<meta http-equiv="refresh" content="3;url=index.html">')
                else:
                    print(f"<p>Error: Username '{username}' already exists.</p>")
                    print('<p>Please choose a different username.</p>')
                    print('<p>Redirecting back to login...</p>')
                    print('<meta http-equiv="refresh" content="3;url=index.html">')
            except Exception as e:
                print(f"<p>Error creating user: {str(e)}</p>")
                print('<p>Redirecting back to login...</p>')
                print('<meta http-equiv="refresh" content="3;url=index.html">')
        else:
            print("<p>Error: Username and password cannot be empty for user creation.</p>")
            print('<p>Redirecting back to login...</p>')
            print('<meta http-equiv="refresh" content="2;url=index.html">')
        print_html_footer()
    else:
        # HTTPヘッダーを出力
        print("Content-Type: text/html; charset=utf-8")
        print() # ヘッダーと本文の間の空行
        
        print_html_header()
        print("<p>Invalid action requested.</p>")
        print('<p>Redirecting back to login...</p>')
        print('<meta http-equiv="refresh" content="2;url=index.html">')
        print_html_footer()

except Exception as e:
    # HTTPヘッダーを出力
    print("Content-Type: text/html; charset=utf-8")
    print() # ヘッダーと本文の間の空行
    
    print_html_header()
    print(f"<p>Database error: {str(e)}</p>")
    print('<p>Redirecting back to login...</p>')
    print('<meta http-equiv="refresh" content="3;url=index.html">')
    print_html_footer()