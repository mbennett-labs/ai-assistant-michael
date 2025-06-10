from calendar_service import GoogleCalendarService
from datetime import datetime

cal = GoogleCalendarService()

# Create your pain management appointment
event = {
    "summary": "Pain Management Appointment",
    "start": {
        "dateTime": "2025-05-30T10:30:00-04:00",
        "timeZone": "America/New_York",
    },
    "end": {
        "dateTime": "2025-05-30T11:30:00-04:00", 
        "timeZone": "America/New_York",
    },
    "description": "Rescheduled pain management appointment"
}

try:
    created_event = cal.service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {created_event.get(htmlLink)}")
except Exception as e:
    print(f"Note: {e}")
    print("(We need write permissions for creating events)")
