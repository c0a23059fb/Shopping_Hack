#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import http.cookies
from utility.database import get_user_by_id, verify_session

def print_login_page():
    """ログインページのHTMLを出力する関数"""
    print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Login</title>
    <style>
        /* --- 全体のスタイルとフォント --- */
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

        /* --- グリッド背景 --- */
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

        /* --- ウィンドウ風コンテナのスタイル --- */
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

        /* --- フォーム要素のスタイル --- */
        .form-group { margin-bottom: 15px; text-align: left;}
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input, .form-group textarea { background-color: #222; border: 1px solid var(--border-color); color: var(--text-color); padding: 8px; width: calc(100% - 20px); font-family: inherit; }
        .form-group input:focus, .form-group textarea:focus { outline: 1px solid var(--text-color); }
        .btn { background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 10px 15px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin-right: 10px; margin-top: 10px; }
        .btn:hover:not(:disabled) { background-color: var(--border-color); color: var(--title-bar-text); }
        .btn:disabled { opacity: var(--disabled-opacity); cursor: not-allowed; }

        /* --- 通知ウィンドウ --- */
        #messageWindow {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 350px;
            height: 180px;
            z-index: 10000;
            display: none;
            border: 2px solid var(--border-color);
            background-color: var(--window-bg);
            box-shadow: 5px 5px 0px rgba(0, 255, 65, 0.3);
            flex-direction: column;
        }
        #messageWindow .title-bar { justify-content: space-between; padding: 4px 8px; }
        #messageWindow .window-content { text-align: center; padding: 15px;}
        #messageText { margin-top: 10px; }
        #messageOkBtn { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar"> <span>[AUTHENTICATE]</span> </div>
        <div class="window-content">
            <p>// WARNING: SQL INJECTION VULNERABILITY DETECTED</p>
            <form id="loginForm" method="POST" action="login.cgi">
                <div class="form-group"> <label for="username">Username</label> <input type="text" id="username" name="username"> </div>
                <div class="form-group"> <label for="password">Password</label> <input type="password" id="password" name="password"> </div>
                <button type="submit" name="action" value="login" class="btn">[login.sh]</button>
                <button type="submit" name="action" value="create_user" class="btn">[create_user.sh]</button>
            </form>
        </div>
    </div>

    <div id="messageWindow">
        <div class="title-bar" id="messageTitle"><span>[SYSTEM_MESSAGE]</span></div>
        <div class="window-content"> <p id="messageText"></p> <button id="messageOkBtn" class="btn">[OK]</button> </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            const loginForm = document.getElementById('loginForm');
            const messageWindow = document.getElementById('messageWindow');
            const messageTitleSpan = messageWindow.querySelector('.title-bar span');
            const messageText = document.getElementById('messageText');
            const messageOkBtn = document.getElementById('messageOkBtn');

            function showMessage(title, text, callback = null) {
                messageTitleSpan.textContent = `[${title}]`;
                messageText.innerHTML = text;
                messageWindow.style.display = 'flex';
                const oldOkBtn = messageOkBtn;
                const newOkBtn = oldOkBtn.cloneNode(true);
                oldOkBtn.parentNode.replaceChild(newOkBtn, oldOkBtn);
                newOkBtn.addEventListener('click', () => {
                    messageWindow.style.display = 'none';
                    if (callback) callback();
                });
            }

            // ログインフォームの初期化
            loginForm.style.display = 'block';
            usernameInput.value = '';
            passwordInput.value = '';
        });
    </script>
</body>
</html>
""")

try:
    # Cookieを取得
    cookie_string = os.environ.get('HTTP_COOKIE', '')
    cookies = http.cookies.SimpleCookie()
    cookies.load(cookie_string)
    
    user_id = None
    session_id = None
    
    # Cookieからuser_idとsession_idを取得
    if 'user_id' in cookies:
        user_id = cookies['user_id'].value
    if 'session_id' in cookies:
        session_id = cookies['session_id'].value
    
    # ログイン状態をチェック
    if user_id and session_id:
        try:
            # セッションが有効かチェック
            if verify_session(user_id, session_id):
                # ログイン済みの場合、home.cgiにリダイレクト
                print("Content-Type: text/html; charset=utf-8")
                print("Location: home.cgi")
                print() # ヘッダーと本文の間の空行
                exit()
        except Exception as e:
            # セッションチェックでエラーが発生した場合はログインページを表示
            pass
    
    # 未ログインの場合、ログインページを表示
    print("Content-Type: text/html; charset=utf-8")
    print() # ヘッダーと本文の間の空行
    print_login_page()

except Exception as e:
    # エラーが発生した場合もログインページを表示
    print("Content-Type: text/html; charset=utf-8")
    print() # ヘッダーと本文の間の空行
    print_login_page()