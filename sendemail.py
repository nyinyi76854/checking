import os
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def send_email():
    # Path to the service account key file
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    
    # Scopes for Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    # Authenticate using the service account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

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
