import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Basic Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "test@example.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "mock_password")

def send_alert_email(recipient: str, subject: str, message_body: str) -> bool:
    """
    Sends an email using configured SMTP credentials.
    In testing/dev without real credentials, it mocks the sending by logging to console.
    """
    if SENDER_EMAIL == "test@example.com" or SENDER_PASSWORD == "mock_password":
        logger.info(f"[MOCK EMAIL] To: {recipient} | Subject: {subject} | Body preview: {message_body[:50]}...")
        # Since this is a local project, explicitly print so the user sees it happens
        print(f"\n====================== NEW EMAIL ALERT ======================")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: \n{message_body}")
        print(f"=============================================================\n")
        return True
        
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message_body, 'html'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")
        return False
