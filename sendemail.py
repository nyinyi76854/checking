import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Email details
    sender_email = 'nyinyilinnhtet399@gmail.com'
    sender_password = 'nyinyi10123'  # Use environment variables in production
    receiver_email = 'biologyq1122@gmail.com'
    subject = "Hi! Biology!"
    body = "Hi! Biology!"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade to secure connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent to {receiver_email}!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    finally:
        server.quit()

if __name__ == "__main__":
    send_email()
