import os
from anthropic import Anthropic
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("../.env")

class AIAssistant:
    def __init__(self):
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment")
        
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        print("AI Assistant brain initialized!")
    
    def chat(self, user_message, calendar_context=None):
        system_prompt = f"""You are Michael's personal AI assistant. You help manage his calendar and provide assistance.

Current date: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}

Calendar context: {calendar_context if calendar_context else 'No current calendar data'}

Be helpful, concise, and professional. Remember all details from our conversation."""

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Keep only last 10 exchanges (20 messages) to stay within limits
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                system=system_prompt,
                messages=self.conversation_history  # Send FULL conversation history
            )
            
            ai_response = response.content[0].text
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    ai = AIAssistant()
    print("Testing AI Assistant...")
    
    response = ai.chat("Hello! What can you help me with?")
    print("AI Response:", response)
