import base64
import json
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
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
    # Load service account credentials
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES) 

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
