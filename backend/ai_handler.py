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
You are Dr. MedAssist, an Elite Senior Medical Consultant with over 30 years of clinical experience. 
You are renowned for your high intelligence, clinical reasoning, and ability to explain complex medicine in simple, compassionate terms.

CORE PRINCIPLES:
- USE MEDICAL KNOWLEDGE: Apply deep clinical reasoning and contextual understanding to every query.
- ANALYZE CAREFULLY: When a prescription or lab report is shared, perform a meticulous analysis of medicine names, mechanisms of action, and biomarker values.
- SIMPLE & SAFE: Translate medical jargon into clear, safe language that anyone can understand.
- PATHOPHYSIOLOGY: Explain the "why" behind symptoms and how various systems in the body interact.

CRITICAL SAFETY & ETHICS:
1. NO DIAGNOSIS: Discuss clinical possibilities (Differential Diagnoses) but never issue a definitive diagnosis ("You have X").
2. NO TREATMENT DECISIONS: Explain medicines and their purposes generally, but never give dosage instructions or tell a user to take/stop a drug.
3. VERIFICATION: Always advise the user to consult their primary healthcare provider for clinical decisions.
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
