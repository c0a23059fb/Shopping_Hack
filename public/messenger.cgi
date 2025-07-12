#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import utility.database as database
import os
import http.cookies

cgitb.enable()

form = cgi.FieldStorage()
action = form.getvalue('action')
recipient = form.getvalue('recipient')
message_content = form.getvalue('message_content')

# セッションチェックと認証チェック
cookie_string = os.environ.get('HTTP_COOKIE', '')
cookies = http.cookies.SimpleCookie()
if cookie_string:
    cookies.load(cookie_string)

is_authenticated, current_user = database.check_authentication(cookies)

if not is_authenticated:
    # 認証されていない場合、ログインページにリダイレクト
    print("Location: index.cgi")
    print()
    exit()

# メッセージ送信処理
if action == 'transmit':
    if recipient and message_content:
        recipient_user = database.get_user_by_username(recipient)
        if recipient_user:
            database.create_message(current_user['id'], recipient_user['id'], message_content)
        else:
            print("Content-Type: text/html; charset=utf-8")
            print()  # ヘッダーと本文の間に空行を追加
            print(f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Terminal X - Messenger Error</title>
</head>
<body>
    <p>Error: User '{recipient}' not found.</p>
    <p><a href="messenger.cgi">[BACK TO MESSENGER]</a></p>
</body>
</html>""")
            exit()
    else:
        print("Content-Type: text/html; charset=utf-8")
        print()  # ヘッダーと本文の間に空行を追加
        print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Terminal X - Messenger Error</title>
</head>
<body>
    <p>Error: Recipient and message cannot be empty.</p>
    <p><a href="messenger.cgi">[BACK TO MESSENGER]</a></p>
</body>
</html>""")
        exit()

# メッセージ表示
messages_data = database.get_messages_for_user(current_user['id'])

print("Content-Type: text/html; charset=utf-8")
print()  # ヘッダーと本文の間に空行を追加
print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal X - Messenger</title>
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
            max-width: 700px;
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
            display: flex;
            flex-direction: column;
        }

        .form-group { margin-bottom: 15px; text-align: left;}
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input, .form-group textarea { background-color: #222; border: 1px solid var(--border-color); color: var(--text-color); padding: 8px; width: calc(100% - 20px); font-family: inherit; }
        .form-group input:focus, .form-group textarea:focus { outline: 1px solid var(--text-color); }
        .btn { background-color: transparent; border: 2px solid var(--border-color); color: var(--text-color); padding: 10px 15px; cursor: pointer; font-family: inherit; text-transform: uppercase; margin-right: 10px; margin-top: 10px; }
        .btn:hover:not(:disabled) { background-color: var(--border-color); color: var(--title-bar-text); }
        .btn:disabled { opacity: var(--disabled-opacity); cursor: not-allowed; }

        #message-display {
            flex-grow: 1;
            border: 1px solid var(--border-color);
            background-color: #000;
            padding: 10px;
            overflow-y: auto;
            margin-bottom: 15px;
            text-align: left;
        }
        .message-item { margin-bottom: 10px; }
        .message-item .sender { font-weight: bold; }
        .message-item .content { padding-left: 10px; word-wrap: break-word; }
        .message-item.sent .sender { color: #00aaff; }
        .message-item.received .sender { color: #ffaa00; }
        #message-form { display: flex; flex-direction: column; }

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
            <span>[SECURE_MESSENGER]</span>
            <a href="home.cgi" class="btn">[HOME]</a>
        </div>
        <div class="window-content">
            <div id="message-display">
""")

# メッセージ表示ロジック
for msg in messages_data:
    is_sent = msg['sender_id'] == current_user['id']
    sender_label = "To" if is_sent else "From"
    sender_name = msg['recipient_name'] if is_sent else msg['sender_name']
    sender_class = "sent" if is_sent else "received"
    print(f'                <div class="message-item {sender_class}">')
    print(f'                    <div class="sender">{sender_label}: {sender_name}</div>')
    print(f'                    <div class="content">&gt; {msg["content"]}</div>')
    print(f'                </div>')

print("""            </div>
            <form id="message-form" method="POST" action="messenger.cgi">
                <input type="hidden" name="action" value="transmit">
                <div class="form-group"> <label for="recipient">To:</label> <input type="text" id="recipient" name="recipient" placeholder="Recipient username..."> </div>
                <div class="form-group"> <label for="message-content">Compose message:</label> <textarea id="message-content" name="message_content" rows="4"></textarea> </div>
                <button type="submit" class="btn">[TRANSMIT]</button>
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
</body>
</html>
""")