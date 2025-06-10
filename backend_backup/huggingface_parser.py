import os
import re
from datetime import datetime, timedelta
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import torch

class HuggingFaceAppointmentParser:
    def __init__(self):
        print("Loading HuggingFace Enhanced Appointment Parser...")
        
        # Initialize models
        self.intent_classifier = None
        self.ner_pipeline = None
        self.sentence_model = None
        self.qa_pipeline = None
        
        self._load_models()
        print("HuggingFace models loaded successfully!")
    
    def _load_models(self):
        """Load HuggingFace models for different tasks"""
        try:
            # 1. Intent Classification - Detect if message is appointment-related
            print("Loading intent classifier...")
            self.intent_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            
            # 2. Named Entity Recognition - Extract dates, times, names
            print("Loading NER pipeline...")
            self.ner_pipeline = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple"
            )
            
            # 3. Sentence Transformer - For semantic understanding
            print("Loading sentence transformer...")
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # 4. Question Answering - Extract specific details
            print("Loading QA pipeline...")
            self.qa_pipeline = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad"
            )
            
        except Exception as e:
            print(f"Error loading some models: {e}")
            print("Falling back to basic parsing...")
    
    def is_appointment_request(self, message):
        """Use AI to detect if message is requesting an appointment"""
        if not self.intent_classifier:
            keywords = ['schedule', 'appointment', 'meeting', 'book', 'reserve']
            return any(keyword in message.lower() for keyword in keywords)
        
        try:
            candidate_labels = [
                "schedule appointment",
                "book meeting", 
                "calendar request",
                "general conversation",
                "question about calendar"
            ]
            
            result = self.intent_classifier(message, candidate_labels)
            top_intent = result['labels'][0]
            confidence = result['scores'][0]
            
            appointment_intents = ["schedule appointment", "book meeting", "calendar request"]
            
            print(f"Intent Analysis: {top_intent} (confidence: {confidence:.2f})")
            
            return top_intent in appointment_intents and confidence > 0.3
            
        except Exception as e:
            print(f"Intent classification error: {e}")
            keywords = ['schedule', 'appointment', 'meeting', 'book', 'reserve']
            return any(keyword in message.lower() for keyword in keywords)
    
    def extract_appointment_details(self, message):
        """Extract appointment details using AI"""
        details = {
            'title': 'Appointment',
            'datetime': None,
            'confidence': 0.0
        }
        
        try:
            # Use QA to extract appointment type
            if self.qa_pipeline:
                qa_result = self.qa_pipeline(
                    question="What type of appointment is this?",
                    context=message
                )
                if qa_result['score'] > 0.1:
                    details['title'] = qa_result['answer'].title() + " Appointment"
                    details['confidence'] += 0.3
            
            # Extract time and date using patterns (enhanced)
            message_lower = message.lower()
            
            # Determine appointment type
            if "dentist" in message_lower:
                details['title'] = "Dentist Appointment"
            elif "doctor" in message_lower:
                details['title'] = "Doctor Appointment"
            elif "meeting" in message_lower:
                details['title'] = "Meeting"
            
            # Determine date
            if "tomorrow" in message_lower:
                appointment_date = datetime.now() + timedelta(days=1)
            elif "today" in message_lower:
                appointment_date = datetime.now()
            else:
                appointment_date = datetime.now() + timedelta(days=1)
            
            # Extract time
            time_match = re.search(r'(\d{1,2})\s*(pm|am|:00)', message_lower)
            if time_match:
                hour = int(time_match.group(1))
                if 'pm' in time_match.group(2) and hour != 12:
                    hour += 12
                elif 'am' in time_match.group(2) and hour == 12:
                    hour = 0
                
                details['datetime'] = appointment_date.replace(
                    hour=hour, minute=0, second=0, microsecond=0
                )
                details['confidence'] += 0.4
            else:
                details['datetime'] = appointment_date.replace(
                    hour=14, minute=0, second=0, microsecond=0
                )
                details['confidence'] += 0.2
            
        except Exception as e:
            print(f"Extraction error: {e}")
        
        return details

# Test the parser
if __name__ == "__main__":
    print("Testing HuggingFace Enhanced Parser:")
    print("=" * 50)
    
    parser = HuggingFaceAppointmentParser()
    
    test_messages = [
        "Schedule a dentist appointment for tomorrow at 2 PM",
        "I need to book a meeting with Dr. Smith next Tuesday at 10 AM", 
        "What's the weather like today?",
        "Book a haircut appointment for this weekend",
        "Can you add a doctor visit to my calendar?"
    ]
    
    for message in test_messages:
        print(f"\nMessage: '{message}'")
        
        # Test intent detection
        is_appointment = parser.is_appointment_request(message)
        print(f"Is appointment request: {is_appointment}")
        
        if is_appointment:
            details = parser.extract_appointment_details(message)
            print(f"Extracted details:")
            print(f"   Title: {details['title']}")
            print(f"   DateTime: {details['datetime']}")
            print(f"   Confidence: {details['confidence']:.2f}")
        
        print("-" * 30)
