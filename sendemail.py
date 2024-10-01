import os
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Fetch the secrets from environment variables
    CLIENT_ID = os.getenv('CLIENT_ID')
    PROJECT_ID = os.getenv('PROJECT_ID')
    AUTH_URI = os.getenv('AUTH_URI')
    TOKEN_URI = os.getenv('TOKEN_URI')
    AUTH_PROVIDER_CERT_URL = os.getenv('AUTH_PROVIDER_CERT_URL')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URIS = os.getenv('REDIRECT_URIS').strip('[]').replace('"', '').split(',')  # Convert string to list
    JAVASCRIPT_ORIGINS = os.getenv('JAVASCRIPT_ORIGINS').strip('[]').replace('"', '').split(',')  # Convert string to list

    # Create the OAuth 2.0 credentials
    credentials = service_account.Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": PROJECT_ID,
        "private_key_id": CLIENT_ID,  # Use CLIENT_ID as a placeholder
        "private_key": CLIENT_SECRET,   # Use CLIENT_SECRET as a placeholder
        "client_email": "chatflow-59776@appspot.gserviceaccount.com",  
        "client_id": CLIENT_ID,
        "auth_uri": AUTH_URI,
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": AUTH_PROVIDER_CERT_URL,
        "redirect_uris": REDIRECT_URIS,
        "javascript_origins": JAVASCRIPT_ORIGINS
    })

    # Scopes for Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Create the Gmail API client
    service = build('gmail', 'v1', credentials=credentials)

    # Email details
    sender_email = 'nyinyilinnhtet399@gmail.com'  # The service account's email
    receiver_email = 'biologyq1122@gmail.com'
    subject = "Hi! Biology!"
    body = "Hi! Biology!"

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Encode the message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        # Send the email
        message = {'raw': raw_message}
        service.users().messages().send(userId='me', body=message).execute()
        print(f"Email sent to {receiver_email}!")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    send_email()
