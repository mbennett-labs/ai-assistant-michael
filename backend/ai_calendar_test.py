from ai_service import AIAssistant
from calendar_service import GoogleCalendarService

print("=== AI + CALENDAR INTEGRATION TEST ===")

# Initialize both services
cal_service = GoogleCalendarService()
ai = AIAssistant()

# Get calendar context
calendar_context = None
try:
    events = cal_service.get_upcoming_events(5)
    if events:
        calendar_context = "Upcoming events:\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            calendar_context += f"- {event.get('summary', 'No Title')} at {start}\n"
except Exception as e:
    calendar_context = "Could not access calendar"

# Test AI with calendar context
questions = [
    "What is my schedule today?",
    "Do I have any appointments this week?"
]

for question in questions:
    print(f"\nUser: {question}")
    response = ai.chat(question, calendar_context)
    print(f"AI: {response}")
