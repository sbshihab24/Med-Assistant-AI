const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const fileInput = document.getElementById('file-upload');
const filePreviewContainer = document.getElementById('file-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeFileBtn = document.getElementById('remove-file-btn');
const loadingOverlay = document.getElementById('loading-overlay');

const API_URL = 'http://127.0.0.1:5000/api/chat';
const sessionId = Math.random().toString(36).substring(7);

let currentBase64Image = null;

// Auto-resize textarea
userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
});

// File Upload Logic
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            currentBase64Image = event.target.result.split(',')[1];
            imagePreview.src = event.target.result;
            filePreviewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

removeFileBtn.addEventListener('click', () => {
    currentBase64Image = null;
    imagePreview.src = '';
    filePreviewContainer.classList.add('hidden');
    fileInput.value = '';
});

// Send Message Logic
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message && !currentBase64Image) return;

    // Append User Message
    appendMessage('user', message || "Shared an image");

    const payload = {
        message: message,
        session_id: sessionId,
        image: currentBase64Image
    };

    // Reset Input
    userInput.value = '';
    userInput.style.height = 'auto';
    removeFileBtn.click(); // Clear preview

    // Show Loader
    showLoader(true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        appendMessage('ai', data.response);
    } catch (error) {
        appendMessage('ai', 'Sorry, I encountered an error. Please make sure the backend server is running.');
        console.error('Error:', error);
    } finally {
        showLoader(false);
    }
}

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;

    // Convert newlines to breaks and simple bolding/links
    const formattedText = text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\[(.*?)\]\s*\((.*?)\)/gs, '<a href="$2" target="_blank" class="chat-link">$1 <i class="fas fa-external-link-alt"></i></a>');

    if (role === 'ai') {
        msgDiv.innerHTML = `
            <img src="logo.png" alt="Avatar" class="avatar">
            <div class="message-content">${formattedText}</div>
        `;
    } else {
        msgDiv.innerHTML = `<div class="message-content">${formattedText}</div>`;
    }

    chatWindow.appendChild(msgDiv);

    // Scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showLoader(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
