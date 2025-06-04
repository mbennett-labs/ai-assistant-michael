import os
from anthropic import Anthropic
from datetime import datetime
from dotenv import load_dotenv
from huggingface_parser import HuggingFaceAppointmentParser

load_dotenv("../.env")

class EnhancedAIAssistant:
    def __init__(self):
        # Initialize Claude
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment")
        
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        
        # Initialize HuggingFace parser
        print("Loading HuggingFace models for enhanced appointment parsing...")
        self.hf_parser = HuggingFaceAppointmentParser()
        
        print("Enhanced AI Assistant initialized!")
    
    def chat(self, user_message, calendar_context=None):
        """Enhanced chat with HuggingFace pre-processing"""
        
        # 1. Use HuggingFace to analyze the message
        is_appointment = self.hf_parser.is_appointment_request(user_message)
        
        # 2. Build enhanced system prompt
        system_prompt = f"""You are Michael's personal AI assistant. You help manage his calendar and provide assistance.

Current date: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}

Calendar context: {calendar_context if calendar_context else 'No current calendar data'}

HuggingFace Analysis: This message {"IS" if is_appointment else "IS NOT"} an appointment request.

Be helpful, concise, and professional."""

        return self._get_claude_response(user_message, system_prompt)
    
    def get_appointment_details_for_creation(self, user_message):
        """Get structured appointment details using HuggingFace"""
        
        if self.hf_parser.is_appointment_request(user_message):
            details = self.hf_parser.extract_appointment_details(user_message)
            
            return {
                'title': details.get('title', 'Appointment'),
                'datetime': details.get('datetime'),
                'description': f"Created via Enhanced AI Assistant from: {user_message}",
                'confidence': details.get('confidence', 0.0),
                'source': 'huggingface_enhanced'
            }
        
        return None
    
    def _get_claude_response(self, user_message, system_prompt):
        """Get response from Claude"""
        
        self.conversation_history.append({"role": "user", "content": user_message})
        
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                system=system_prompt,
                messages=self.conversation_history
            )
            
            ai_response = response.content[0].text
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Testing Enhanced AI Assistant...")
    ai = EnhancedAIAssistant()
    
    response = ai.chat("Schedule a dentist appointment for tomorrow at 2 PM")
    print("AI Response:", response)
