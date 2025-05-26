import os
from dotenv import load_dotenv

print("Current directory:", os.getcwd())
print("Looking for .env at:", os.path.abspath("../.env"))
print("Does .env exist?", os.path.exists("../.env"))

load_dotenv("../.env")  # Explicitly specify the path
api_key = os.getenv("CLAUDE_API_KEY")
print("API Key found:", "Yes" if api_key else "No")
if api_key:
    print("Key starts with:", api_key[:15])
