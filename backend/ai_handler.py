import os
import openai
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return openai.OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
4. EMERGENCY TRIAGE: Immediately prioritize emergency room advice for red-flag symptoms (chest pain, stroke signs, etc.).

For any question regarding news, updates, or current events, rely strictly on the external search context provided (if any). Always include a medical disclaimer.
"""

def get_ai_response(messages, model="gpt-4o"):
    """
    Sends the message history to OpenAI and returns the AI's response.
    """
    client = get_client()
    if not client:
        return "⚠️ **Configuration Error**: OpenAI API Key is missing. Please add it to your `.env` file in the backend folder and restart the server."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def format_image_message(text, base64_image):
    """
    Formats a message with text and an image for GPT-4o Vision.
    """
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": text},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    }
