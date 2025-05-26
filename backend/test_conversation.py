from ai_service import AIAssistant

ai = AIAssistant()
print("=== TESTING YOUR AI ASSISTANT ===")

# Test different questions
questions = [
    "What can you help me with today?",
    "How would you schedule a meeting for me?",
    "Tell me about your capabilities"
]

for question in questions:
    print(f"\nUser: {question}")
    response = ai.chat(question)
    print(f"AI: {response}")
