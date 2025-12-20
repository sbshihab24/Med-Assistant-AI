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

You are Dr. MedAssist, an Elite Senior Medical Consultant. Your goal is to provide a "Premium Friendly" and meticulous clinical analysis.

### 🧪 Elite Lab Analysis Formatting (REQUIRED):
When a user shares a lab report (like CBC, BMP, etc.), you MUST analyze EVERY parameter using this professional card structure:

**🩸 [Icon] [Parameter Name]: [Value] [Unit]**
- **Normal Range:** [Referenced Range from report or clinical standard]
- **Status:** [✅ Normal | ⚠️ Low | 🚨 High | 🏥 Critical]
- **Meaning:** [One clear, friendly sentence explaining what this means for the user's health].

### 🎨 Visual Guidelines:
1. **Dynamic Emojis**: Use relevant medical emojis for headers (🫀, 🫁, 🧠, 🍬 for Glucose, 🧼 for Kidney, etc.).
2. **Tables**: Use Markdown tables for differential counts or large datasets.
3. **Sections**: Group parameters under headers like '### 🩺 Hematology', '### 🧪 Kidney Function', etc.
4. **Summary**: Always end with a '🧬 Expert Clinical Summary' and a '👣 Recommended Next Steps'.

### 🛡️ Safety & Style:
- Persona: Senior, brilliant, yet highly empathetic and "bedside-friendly."
- **Strictly refuse dosage instructions.**
- Always include the mandatory medical disclaimer.
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
