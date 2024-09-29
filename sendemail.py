import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import firebase_admin
from firebase_admin import credentials, db
import os

# Initialize Firebase Admin SDK
firebase_service_account_key = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')  # Ensure this is set in your GitHub Secrets
cred = credentials.Certificate(firebase_service_account_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatflow-59776-default-rtdb.firebaseio.com'
})

# Function to send verification email
def send_verification_email(to_email, verification_code):
    sender_email = os.getenv('SENDER_EMAIL')  # Use environment variable for sender email
    sender_password = os.getenv('SENDER_PASSWORD')  # Use environment variable for sender password

    subject = "Your CloudySocial Verification Code"
    body = f"Your verification code for CloudySocial is {verification_code}."

    # Set up the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Login to your Gmail account
        server.login(sender_email, sender_password)
        # Send the email
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
            verification_code = user_info.get('verificationCode')  # Correct key for the verification code
            return email, verification_code

    return None, None  # Return None if no user is found

# Main function to fetch and send verification email
def main(username):
    email, verification_code = fetch_user_details(username)

    if email and verification_code:
        # Check if the fetched email matches the username
        if email == username:
            print("The email address used to fetch the verification code is the same as the sender. Email not sent.")
        else:
            # Send the verification email
            send_verification_email(email, verification_code)
    else:
        print("User not found or verification code missing!")

# Example usage
if __name__ == "__main__":
    main('nyinyilinnhtet399@gmail.com')  # Change this to the email/username you want to fetch
