from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
import os
import hashlib
import secrets
import time
from datetime import datetime, timedelta
sys.path.append('../backend')

from enhanced_ai_service import EnhancedAIAssistant
from calendar_service import GoogleCalendarService
import re

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Quantum Security Users
QUANTUM_USERS = {
    'michael': {
        'password': 'bloc_nut_1972',  # Change this!
        'access_level': 'admin',
        'calendar_access': True
    },
    'demo': {
        'password': 'demo123',
        'access_level': 'user', 
        'calendar_access': False
    }
}

SESSION_TIMEOUT = 1800  # 30 minutes

# Initialize services (your exact working code)
print("Initializing Enhanced AI Assistant with HuggingFace...")
ai_assistant = EnhancedAIAssistant()
calendar_service = GoogleCalendarService()

def check_session_valid():
    if 'user_id' not in session or 'last_activity' not in session:
        return False
    if time.time() - session['last_activity'] > SESSION_TIMEOUT:
        session.clear()
        return False
    session['last_activity'] = time.time()
    return True

def require_auth(f):
    def decorated_function(*args, **kwargs):
        if not check_session_valid():
            return jsonify({'error': 'Authentication required', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def home():
    if not check_session_valid():
        return redirect(url_for('login'))
    return render_template('index.html', user=session.get('user_id'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.json.get('username', '').lower()
    password = request.json.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'})
    
    user = QUANTUM_USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'success': False, 'error': 'Invalid credentials'})
    
    session['user_id'] = username
    session['access_level'] = user['access_level']
    session['last_activity'] = time.time()
    session['login_time'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True, 
        'message': 'Quantum authentication successful',
        'access_level': user['access_level'],
        'calendar_access': user['calendar_access']
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# YOUR EXACT WORKING ROUTES WITH AUTH PROTECTION
@app.route('/chat', methods=['POST'])
@require_auth
def chat():
    try:
        user_message = request.json.get('message', '')
        
        # Check if user has full AI access
        if session.get('access_level') != 'admin':
            return jsonify({
                'success': True,
                'response': 'Demo mode: AI assistant available for admin users. This showcases the quantum-secured interface.',
                'demo_mode': True
            })
        
        # Get calendar context (your exact code)
        calendar_context = get_calendar_context()
        
        # Use HuggingFace enhanced appointment creation (your exact code)
        appointment_created = False
        appointment_details = ai_assistant.get_appointment_details_for_creation(user_message)
        
        if appointment_details and appointment_details['confidence'] > 0.5:
            result = create_appointment(appointment_details)
            if result:
                appointment_created = True
        
        # Get enhanced AI response (your exact code)
        ai_response = ai_assistant.chat(user_message, calendar_context)
        
        # If we created an appointment, mention it (your exact code)
        if appointment_created:
            confidence_pct = int(appointment_details['confidence'] * 100)
            ai_response += f"\n\nSUCCESS: I've created this appointment in your Google Calendar! (AI Confidence: {confidence_pct}%)"
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'appointment_created': appointment_created,
            'hf_analysis': appointment_details is not None,
            'confidence': appointment_details['confidence'] if appointment_details else 0,
            'quantum_secured': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/calendar-events')
@require_auth
def calendar_events():
    try:
        # Check calendar access
        user = QUANTUM_USERS.get(session.get('user_id'))
        if not user or not user['calendar_access']:
            return jsonify({
                'success': False,
                'error': 'Calendar access not available for this user level'
            })
        
        # Your exact working code
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

@app.route('/status')
@require_auth
def status():
    user = QUANTUM_USERS.get(session.get('user_id'))
    return jsonify({
        'user': session.get('user_id'),
        'access_level': session.get('access_level'),
        'session_time': time.time() - session.get('last_activity', 0),
        'calendar_access': user['calendar_access'] if user else False,
        'login_time': session.get('login_time')
    })

# YOUR EXACT WORKING FUNCTIONS
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
    print("Starting Quantum-Secured AI Assistant Web Interface with HuggingFace")
    app.run(host="0.0.0.0", port=5000, debug=False)
