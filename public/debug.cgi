#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import http.cookies
from datetime import datetime

# utilityディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'utility'))
from database import get_session

cgitb.enable()

print("Content-Type: text/html; charset=utf-8")
print()

print("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Debug Info</title>
</head>
<body>
    <h1>Debug Information</h1>
""")

# 環境変数の確認
print(f"<p><strong>HTTP_COOKIE:</strong> {os.environ.get('HTTP_COOKIE', 'No cookies found')}</p>")

# Cookieの解析
cookie_string = os.environ.get('HTTP_COOKIE', '')
cookies = http.cookies.SimpleCookie()
if cookie_string:
    cookies.load(cookie_string)
    session_id = cookies.get('session_id')
    if session_id:
        session_id_value = session_id.value
        print(f"<p><strong>Session ID:</strong> {session_id_value}</p>")
        
        # データベースでセッション確認
        try:
            session = get_session(session_id_value)
            if session:
                print(f"<p><strong>Session found:</strong> User ID: {session['user_id']}, Expires: {session['expires_at']}</p>")
                print(f"<p><strong>Current time:</strong> {datetime.now()}</p>")
            else:
                print("<p><strong>Session not found or expired</strong></p>")
        except Exception as e:
            print(f"<p><strong>Database error:</strong> {str(e)}</p>")
    else:
        print("<p><strong>No session_id in cookies</strong></p>")
else:
    print("<p><strong>No cookies found</strong></p>")

print("""
</body>
</html>
""")
