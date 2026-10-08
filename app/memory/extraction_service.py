import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GEMINI_API_KEY")
)

def extract_memories(user_message):
    prompt = f"""
You are a memory extraction system. 
    
Extract useful, long-term facts about the user 
from the message below. 
    
Rules: 1. Extract each fact as a separate memory. 
2. Ignore greetings, small talk, and temporary details. 
3. Do not invent facts. 
4. Return an empty list if nothing is worth remembering. 
5. Return only valid JSON, with no markdown. 
6. Use "semantic" for facts, preferences, goals, 
    skills, and background information. 
7. Use an importance score from 1 to 10. 
    
Use this JSON format: 
[ 
    {{ 
        "memory_text": "User studies AIML", 
        "memory_type": "semantic", 
        "importance_score": 9 
    }} 
] 
    
User message: 
{user_message}
"""
    
    response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt
    )
    
    return json.loads(response.text)
