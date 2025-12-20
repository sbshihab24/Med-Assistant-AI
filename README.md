# 🏥 MedAssist AI – Elite Senior Medical Consultant Assistant

MedAssist AI is a production-grade, full-stack medical chatbot designed to provide clean, safe, and professional medical information. Built for recruiters and medical AI enthusiasts, it features a premium UI, robust safety protocols, and advanced AI capabilities including OCR for prescriptions and a dedicated Medical News Agent.

---

## 🌟 Key Features

### 🖥️ Premium Medical UI
- **Modern Aesthetic**: Clean white, medical blue, and soft green palette.
- **Messenger-Style Chat**: Smooth animations, user/AI message separation, and auto-scroll.
- **Fully Responsive**: Optimized for both Desktop and Mobile experiences.
- **File Previews**: Live preview of uploaded medical documents before sending.

### 🧠 Advanced Medical Intelligence
- **AI Safety First**: Persistent medical disclaimer and safety-tuned system prompts.
- **OCR Document Analysis**: Uses GPT-4o Vision to extract and explain text from prescriptions and lab reports.
- **Medical News Agent**: Dedicated agent to fetch latest healthcare updates with source/date labeling.
- **Conversation Memory**: Context-aware sessions for natural follow-up questions.

---

## 🛠️ Technology Stack

### **Frontend**
- **HTML5 & CSS3**: Vanilla implementation with Flexbox/Grid for maximum performance.
- **Vanilla JavaScript**: Pure JS for chat logic and API communication (no heavy frameworks).
- **FontAwesome**: High-quality medical and interface iconography.
- **Inter Font**: Premium typography for readability.

### **Backend**
- **Python Flask**: Secure and lightweight API backend.
- **OpenAI API**: Powering chat, vision, and information retrieval.
- **python-dotenv**: Environment-based security for API keys.
- **Flask-CORS**: Enabled for secure cross-origin communication.

---

## ⚙️ Installation & Setup

### 1️⃣ Backend Setup
1. Open your terminal in the **project root** directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Configure your `.env` file (ensure it's in the `backend/` folder):
   - Add your `OPENAI_API_KEY`.
5. Run the server:
   ```bash
   cd backend
   python app.py
   ```

### 2️⃣ Frontend Setup
1. No installation required!
2. Simply open `frontend/index.html` in any modern web browser.
3. Start chatting with MedAssist AI.

---

## 🛡️ AI Safety & Ethics
- **No Diagnosis**: The AI is strictly prohibited from diagnosing or prescribing.
- **Empathetic Tone**: Uses calm, supportive language.
- **Always Verify**: Includes mandatory reminders to consult professional healthcare providers.
- **Data Privacy**: Session-based memory only; no permanent storage of medical documents.

---

## 📂 Project Structure
```text
MedAssist-AI/
├── frontend/
│   ├── index.html       # Main UI structure
│   ├── style.css        # Premium medical styling
│   └── script.js        # Chat logic & API calls
├── backend/
│   ├── app.py           # Flask server & routes
│   ├── ai_handler.py    # OpenAI & Safety logic
│   ├── news_agent.py    # Medical News Intelligence
│   ├── requirements.txt # Python dependencies
│   └── .env             # API Keys & Secrets
└── README.md            # Project documentation
```

---

## 📜 License
This project is for educational and portfolio purposes. 
**Disclaimer**: MedAssist AI is an information tool and NOT a medical diagnostic device.

---

👨‍💻 **Author**  
**Mehedi Hasan Shihab**  
AI Developer | Machine Learning & LLM Systems  

🔗 **GitHub**: [sbshihab24](https://github.com/sbshihab24)  
🔗 **LinkedIn**: [shihab24](https://www.linkedin.com/in/shihab24)
