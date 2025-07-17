#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import http.cookies

# from utility.database import verify_session # DB参照はしないためコメントアウト
cgitb.enable()

# --- 仮の認証チェック ---
# 本来はここでセッションを検証するが、今は常に認証済みとして扱う
is_authenticated = True
# current_user = {'username': 'testuser'} # 仮のユーザー情報

if not is_authenticated:
    # 認証されていない場合、ログインページにリダイレクト
    print("Location: index.cgi")
    print()
    exit()


# --- HTML出力 ---
print("Content-Type: text/html; charset=utf-8")
print()

print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Account Settings</title>
    <style>
        /* home.cgiと同じスタイルを適用 */
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Inconsolata&display=swap');
        :root {
            --background-color: #0a0a0a;
            --text-color: #00ff41;
            --border-color: #00ff41;
            --window-bg: #111111;
            --title-bar-bg: #00ff41;
            --title-bar-text: #0a0a0a;
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
            max-width: 600px; /* 少し幅を調整 */
            width: 90%;
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
            padding: 25px;
            overflow-y: auto;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        input[type="password"] {
            background-color: #222;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 10px;
            width: calc(100% - 24px);
            font-family: inherit;
            font-size: 1em;
        }
        .btn {
            background-color: transparent;
            border: 2px solid var(--border-color);
            color: var(--text-color);
            padding: 10px 15px;
            cursor: pointer;
            font-family: inherit;
            text-transform: uppercase;
            margin-top: 10px;
        }
        .btn:hover {
            background-color: var(--border-color);
            color: var(--title-bar-text);
        }
        .home-link {
            color: var(--text-color);
            text-decoration: none;
            border: 1px solid var(--text-color);
            padding: 5px 10px;
        }
    </style>
</head>
<body>
    <div class="window-container">
        <div class="title-bar">
            <span>[ACCOUNT_SETTINGS]</span>
            <a href="home.cgi" class="home-link">[HOME]</a>
        </div>
        <div class="window-content">
            <form id="passwordChangeForm" method="POST" action="account.cgi">
                <input type="hidden" name="action" value="change_password">
                
                <div class="form-group">
                    <label for="current_password">Current Password:</label>
                    <input type="password" id="current_password" name="current_password">
                </div>
                
                <div class="form-group">
                    <label for="new_password">New Password:</label>
                    <input type="password" id="new_password" name="new_password" required>
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">Confirm New Password:</label>
                    <input type="password" id="confirm_password" name="confirm_password" required>
                </div>
                
                <button type="submit" class="btn">[UPDATE_PASSWORD]</button>
            </form>
        </div>
    </div>
</body>
</html>
""")
