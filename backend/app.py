import os
import secrets
import base64
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from ai_handler import get_ai_response, format_image_message
from news_agent import get_medical_news, is_news_query
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(16))
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "MedAssist AI API is running. Use /api/chat for assistant interactions.",
        "author": "Mehedi Hasan Shihab"
    })

# In-memory session store (In production, use Redis or a DB)
# Key: session_id, Value: list of messages
chat_history = {}

def get_session_history(session_id):
    if session_id not in chat_history:
        chat_history[session_id] = []
    # Keep only last 10 messages for context
    return chat_history[session_id][-10:]

def update_session_history(session_id, role, content):
    if session_id not in chat_history:
        chat_history[session_id] = []
    chat_history[session_id].append({"role": role, "content": content})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    image_data = data.get('image') # Base64 string if present

    # Check if it's a news query
    if is_news_query(user_message) and not image_data:
        news_response = get_medical_news(user_message)
        update_session_history(session_id, "user", user_message)
        update_session_history(session_id, "assistant", news_response)
        return jsonify({"response": news_response})

    # Prepare message history
    history = get_session_history(session_id)
    
    if image_data:
        # If image exists, we use Vision
        # Note: Vision doesn't always support long histories well, so we focus on the current image
        current_msg = format_image_message(user_message or "Analyze this medical document.", image_data)
        ai_response = get_ai_response([current_msg])
    else:
        # Regular text chat
        update_session_history(session_id, "user", user_message)
        history.append({"role": "user", "content": user_message})
        ai_response = get_ai_response(history)

    update_session_history(session_id, "assistant", ai_response)
    
    return jsonify({"response": ai_response})

@app.route('/api/clear', methods=['POST'])
def clear_session():
    session_id = request.json.get('session_id', 'default')
    if session_id in chat_history:
        del chat_history[session_id]
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
