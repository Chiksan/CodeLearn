import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings


def send_verification_email(to_email: str, username: str, token: str):
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[EMAIL] Код верификации для {to_email}: {token}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Код подтверждения — CodeLearn"
    msg["From"]    = settings.SMTP_USER
    msg["To"]      = to_email

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;padding:32px 24px;background:#fff">
      <div style="text-align:center;margin-bottom:28px">
        <span style="font-size:28px;font-weight:800;color:#534AB7">&lt;/&gt; CodeLearn</span>
      </div>
      <h2 style="color:#1a1a1a;margin-bottom:12px">Привет, {username}! 👋</h2>
      <p style="color:#555;font-size:15px;line-height:1.65">
        Введи этот код на сайте чтобы подтвердить свой email:
      </p>
      <div style="text-align:center;margin:32px 0">
        <div style="display:inline-block;padding:20px 40px;background:#f4f3ff;border:2px solid #534AB7;
                    border-radius:14px;">
          <span style="font-size:40px;font-weight:800;color:#534AB7;letter-spacing:10px">{token}</span>
        </div>
      </div>
      <p style="color:#aaa;font-size:13px;text-align:center">
        Код действителен 24 часа. Если ты не регистрировался — просто проигнори это письмо.
      </p>
    </div>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False
