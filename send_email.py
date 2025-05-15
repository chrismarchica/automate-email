from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os.path
import base64
from email.mime.text import MIMEText
import time
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message, recipient_email):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {message['id']}")
        print(f"Email sent successfully to {recipient_email}!")
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Get Gmail API service
    service = get_gmail_service()
    
    # Load JSON data
    with open(input("Enter the path to the JSON file: "), 'r') as file:
        data = json.load(file)
    
    # Email details
    sender = input("Enter your email: ") 
    for entry in data:
        to = entry['email']
        # Use TikTok handle for personalization
        first_name = entry['tiktok_handle']
        subject = f"Social Media Campaign for {entry['song_title']}"
        message_text = (
            f"Hi {first_name},\n\n"
            f"We came across your page from when you used {entry['song_title']} and love your content! "
            f"We think you would be a great fit for our campaign with {entry['artist']} and {entry['song_title']}. "
            f"How much do you charge for a 1x TikTok promo?\n\n"
            f"Thank you,\n"
            f"{entry['label']}"
        )
        message = create_message(sender, to, subject, message_text)
        send_message(service, "me", message, to)
        time.sleep(1)  # Wait for 1 second before sending the next email

if __name__ == '__main__':
    main()
