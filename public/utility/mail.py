import smtplib
from email.mime.text import MIMEText
from email.header import Header

def load_message_template(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ テンプレートファイルが見つかりませんでした。")
        return ""

def SentMail_LoadFileVer(name: str, to_address: str, file_name: str):
    from_address = "test@example.com" 
    smtp_host = "sandbox.smtp.mailtrap.io"
    smtp_port = 587
    smtp_user = "4d4d048963342e"
    smtp_pass = "2eaaddb60022c9"

    # 件名とテンプレート読み込み
    subject = f"{name}さんの予約内容"
    body = load_message_template(file_name)
    if not body:
        return  # ファイルがないなら中断

    # メールメッセージ作成（UTF-8で日本語対応）
    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = from_address
    msg["To"] = to_address

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        #print("✅ メール送信成功！")
    except Exception as e:
        print("❌ メール送信失敗！")
        print("🔍 エラー:", e)

def SentMail_NomalVer(to_address: str, message: str):
    from_address = "test@example.com" 
    smtp_host = "sandbox.smtp.mailtrap.io"
    smtp_port = 587
    smtp_user = "4d4d048963342e"
    smtp_pass = "2eaaddb60022c9"

    subject = f"購入確定通知"
    body = message

    # メールメッセージ作成（UTF-8で日本語対応）
    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = from_address
    msg["To"] = to_address

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        #print("✅ メール送信成功！")
    except Exception as e:
        print("❌ メール送信失敗！")
        print("🔍 エラー:", e)

if __name__ == "__main__":
    # テスト用のメール送信
    SentMail_NomalVer("c0a2302749@apps.edu.teu.ac.jp", "テストメールの内容です。<script>alert('test')</script>")