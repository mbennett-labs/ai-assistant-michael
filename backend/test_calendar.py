from calendar_service import GoogleCalendarService
from datetime import datetime

print("Testing calendar connection...")
cal = GoogleCalendarService()
print("Calendar service created successfully!")

try:
    events = cal.service.events().list(
        calendarId='primary',
        maxResults=5,
        singleEvents=True,
        orderBy='startTime',
        timeMin=datetime.utcnow().isoformat() + 'Z'
    ).execute()
    
    events_list = events.get('items', [])
    print(f"Found {len(events_list)} upcoming events!")
    
    for event in events_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"- {event.get('summary', 'No Title')} at {start}")
        
except Exception as e:
    print(f"Error: {e}")
    
print("Calendar test complete!")
