import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import firebase_admin
from firebase_admin import credentials, db
import os
import json
import tempfile

# Function to write the service account key to a temporary file
def get_service_account_credentials():
    firebase_service_account_key = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
    # Write the service account key to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(firebase_service_account_key.encode('utf-8'))
        temp_file_path = temp_file.name
    return temp_file_path

# Initialize Firebase Admin SDK
cred = credentials.Certificate(get_service_account_credentials())
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatflow-59776-default-rtdb.firebaseio.com'
})

# Function to send verification email
def send_verification_email(to_email, verification_code):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    subject = "Your CloudySocial Verification Code"
    body = f"Your verification code for CloudySocial is {verification_code}."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}!")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Fetch user email and verification code from Firebase Realtime Database
def fetch_user_details(username):
    ref = db.reference('users')
    users_data = ref.get()

    for user_id, user_info in users_data.items():
        if user_info.get('email') == username or user_id == username:
            email = user_info.get('email')
            verification_code = user_info.get('verificationCode')
            return email, verification_code

    return None, None

# Main function to fetch and send verification email
def main(username):
    email, verification_code = fetch_user_details(username)

    if email and verification_code:
        send_verification_email(email, verification_code)
    else:
        print("User not found or verification code missing!")

if __name__ == "__main__":
    main('nyinyilinnhtet399@gmail.com')
