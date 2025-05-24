import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

# Add write permissions
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

class GoogleCalendarService:
    def __init__(self):
        print("Starting Google Calendar setup...")
        self.authenticate()
    
    def authenticate(self):
        creds = None
        if os.path.exists('../config/token.pickle'):
            with open('../config/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('../config/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('../config/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
        print("Google Calendar connected successfully!")
