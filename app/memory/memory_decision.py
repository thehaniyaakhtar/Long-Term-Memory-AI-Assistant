import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GEMINI_API_KEY")
    
)

def should_remember(user_message):
    prompt = f"""
You are deciding whether an AI assistant should
remember something about the user.

Remember information when it is:
- Personal and likely useful later
- A long-term preference
- A goal
- A skill or area of study
- A recurring interest
- Important background information

Do NOT remember:
- Greetings
- Small talk
- Temporary situations
- One-time actions
- Random facts that do not describe the user

Return ONLY:
YES
or
NO

User message:
{user_message}
"""
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    
    answer = response.text.strip().upper()
    
    return answer == "YES"