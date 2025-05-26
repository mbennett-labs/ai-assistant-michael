import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
from datetime import datetime, timedelta

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'  # This allows creating events
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
    
    def get_upcoming_events(self, max_results=10):
        """Get upcoming calendar events."""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
            
        except Exception as error:
            print(f'Calendar error: {error}')
            return []
    
    def create_event(self, title, date_time, duration_hours=1, description=""):
        """Create a new calendar event."""
        try:
            # Parse the date_time if it's a string
            if isinstance(date_time, str):
                start_time = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
            else:
                start_time = date_time
            
            end_time = start_time + timedelta(hours=duration_hours)
            
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'America/New_York',
                },
            }
            
            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f'Event created: {event_result.get("htmlLink")}')
            return event_result
            
        except Exception as error:
            print(f'Error creating event: {error}')
            return None

if __name__ == "__main__":
    cal = GoogleCalendarService()
    print("Calendar service ready!")
