from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append('../backend')

from enhanced_ai_service import EnhancedAIAssistant
from calendar_service import GoogleCalendarService
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Initialize services
print("Initializing Enhanced AI Assistant with HuggingFace...")
ai_assistant = EnhancedAIAssistant()
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
        
        # Use HuggingFace enhanced appointment creation
        appointment_created = False
        appointment_details = ai_assistant.get_appointment_details_for_creation(user_message)
        
        if appointment_details and appointment_details['confidence'] > 0.5:
            result = create_appointment(appointment_details)
            if result:
                appointment_created = True
        
        # Get enhanced AI response
        ai_response = ai_assistant.chat(user_message, calendar_context)
        
        # If we created an appointment, mention it
        if appointment_created:
            confidence_pct = int(appointment_details['confidence'] * 100)
            ai_response += f"\n\nSUCCESS: I've created this appointment in your Google Calendar! (AI Confidence: {confidence_pct}%)"
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'appointment_created': appointment_created,
            'hf_analysis': appointment_details is not None,
            'confidence': appointment_details['confidence'] if appointment_details else 0
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

def create_appointment(appointment_details):
    """Create appointment using HuggingFace extracted details"""
    try:
        result = calendar_service.create_event(
            title=appointment_details['title'],
            date_time=appointment_details['datetime'],
            duration_hours=1,
            description=appointment_details['description']
        )
        print(f"Appointment created with HuggingFace confidence: {appointment_details['confidence']:.2f}")
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
    print("Starting Enhanced AI Assistant Web Interface with HuggingFace")
    app.run(debug=True, port=5001)
