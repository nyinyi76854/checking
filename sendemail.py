import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_email(sender_email, receiver_email, smtp_server, smtp_port, login, password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Test Email from Python Script"

    body = "This is a test email sent from a Python script!"
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    sender_email = os.environ.get("EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    login = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")

    send_test_email(sender_email, receiver_email, smtp_server, smtp_port, login, password)
