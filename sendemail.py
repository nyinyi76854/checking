import base64
import os
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}

def send_email():
    """Sends an email using the Gmail API."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        sender_email = "nyinyilinnhtet399@gmail.com"  # Replace with your Gmail address 
        receiver_email = "thetthetmaw10123@gmail.com"  # Replace with the recipient's email address 
        subject = "Test Email"
        message_text = "This is a test email sent from Python."

        # Create the email message
        message = create_message(sender_email, receiver_email, subject, message_text)

        # Send the email
        message = (service.users().messages().send(userId="me", body=message).execute())
        print(f"Message sent successfully with Id: {message['id']}")

    except HttpError as error:
        print(f'An error occurred: {error}')

send_email()
