from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append('../backend')

from ai_service import AIAssistant
from calendar_service import GoogleCalendarService
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Initialize services
print("Initializing AI Assistant and Calendar Service...")
ai_assistant = AIAssistant()
calendar_service = GoogleCalendarService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        # Get calendar context
        calendar_context = get_calendar_context()
        
        # Check if this is an appointment creation request
        appointment_created = False
        if should_create_appointment(user_message):
            appointment_info = extract_appointment_info(user_message)
            if appointment_info:
                result = create_appointment(appointment_info)
                if result:
                    appointment_created = True
        
        # Get AI response
        ai_response = ai_assistant.chat(user_message, calendar_context)
        
        # If we created an appointment, mention it
        if appointment_created:
            ai_response += "\n\n✅ I've successfully created this appointment in your Google Calendar!"
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'appointment_created': appointment_created
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/calendar-events')
def calendar_events():
    try:
        events = calendar_service.get_upcoming_events(50)
        return jsonify({
            'success': True,
            'events': events
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def should_create_appointment(message):
    """Check if the message is requesting to create an appointment"""
    keywords = ['schedule', 'appointment', 'meeting', 'book', 'add to calendar']
    return any(keyword in message.lower() for keyword in keywords)

def extract_appointment_info(message):
    """Extract appointment details from the message"""
    # This is a simple parser - in production you'd use more sophisticated NLP
    message_lower = message.lower()
    
    # Look for appointment type
    title = "Appointment"
    if "dentist" in message_lower:
        title = "Dentist Appointment"
    elif "doctor" in message_lower:
        title = "Doctor Appointment"
    elif "meeting" in message_lower:
        title = "Meeting"
    
    # Look for time references
    if "tomorrow" in message_lower:
        appointment_date = datetime.now() + timedelta(days=1)
    elif "today" in message_lower:
        appointment_date = datetime.now()
    else:
        appointment_date = datetime.now() + timedelta(days=1)  # Default to tomorrow
    
    # Look for specific times
    time_match = re.search(r'(\d{1,2})\s*(pm|am|:00)', message_lower)
    if time_match:
        hour = int(time_match.group(1))
        if 'pm' in time_match.group(2) and hour != 12:
            hour += 12
        elif 'am' in time_match.group(2) and hour == 12:
            hour = 0
        
        appointment_date = appointment_date.replace(hour=hour, minute=0, second=0, microsecond=0)
    else:
        appointment_date = appointment_date.replace(hour=14, minute=0, second=0, microsecond=0)  # Default 2 PM
    
    return {
        'title': title,
        'datetime': appointment_date,
        'description': f"Created via AI Assistant from: {message}"
    }

def create_appointment(appointment_info):
    """Actually create the appointment in Google Calendar"""
    try:
        result = calendar_service.create_event(
            title=appointment_info['title'],
            date_time=appointment_info['datetime'],
            duration_hours=1,
            description=appointment_info['description']
        )
        return result is not None
    except Exception as e:
        print(f"Error creating appointment: {e}")
        return False

def get_calendar_context():
    try:
        events = calendar_service.get_upcoming_events(5)
        if events:
            context = "Upcoming events:\n"
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                context += f"- {event.get('summary', 'No Title')} at {start}\n"
            return context
    except Exception as e:
        return "Could not access calendar"
    return "No upcoming events"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
