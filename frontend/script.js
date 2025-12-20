const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const fileInput = document.getElementById('file-upload');
const filePreviewContainer = document.getElementById('file-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeFileBtn = document.getElementById('remove-file-btn');
const loadingOverlay = document.getElementById('loading-overlay');

// Use current origin for API calls (One-Link setup)
const API_BASE_URL = window.location.origin;
const API_URL = `${API_BASE_URL}/api/chat`;
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
        const fileType = file.type;
        const fileName = file.name;

        // Show file visual
        filePreviewContainer.classList.remove('hidden');

        if (fileType.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (event) => {
                currentBase64Image = event.target.result.split(',')[1];
                imagePreview.src = event.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            // For non-image files (PDF, CSV, etc.)
            imagePreview.src = 'https://cdn-icons-png.flaticon.com/512/2991/2991108.png'; // Document Icon
            currentBase64Image = "DOCUMENT_PLACEHOLDER"; // Signal to backend if we add doc processing
            // Note: GPT-4o Vision still needs images. For now we show the doc icon.
        }
    }
});

// Send Message Logic
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message && !currentBase64Image) return;

    // Append User Message
    appendMessage('user', message || "Shared a document", currentBase64Image && currentBase64Image !== "DOCUMENT_PLACEHOLDER" ? imagePreview.src : null);

    const payload = {
        message: message,
        session_id: sessionId,
        image: currentBase64Image
    };

    // Reset Input
    userInput.value = '';
    userInput.style.height = 'auto';
    removeFileBtn.click(); // Clear preview

    // Show Thinking Bubble
    const thinkingBubble = showThinkingBubble();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        thinkingBubble.remove();
        appendMessage('ai', data.response);
    } catch (error) {
        thinkingBubble.remove();
        appendMessage('ai', 'Sorry, I encountered an error. Please make sure the backend server is running.');
        console.error('Error:', error);
    }
}

function showThinkingBubble() {
    const bubble = document.createElement('div');
    bubble.className = 'thinking-bubble';
    bubble.innerHTML = `<img src="logo.png" style="width:24px; height:24px;"><span>Dr. MedAssist is analyzing...</span>`;
    chatWindow.appendChild(bubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return bubble;
}

function appendMessage(role, text, imageUrl = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;

    // Map Headers to Medical Emojis
    const headerIcons = {
        'Blood': '🩸',
        'Lab': '🧪',
        'Leukocyte': '🔬',
        'Immune': '🛡️',
        'Heart': '🫀',
        'Brain': '🧠',
        'Lung': '🫁',
        'Bone': '🦴',
        'Kidney': '🧼',
        'Sugar': '🍬',
        'Next Steps': '👣',
        'Warning': '⚠️',
        'Critical': '🚨'
    };

    // Convert headers (### Header) to styled divs with dynamic icons
    let formattedText = text
        .replace(/^###\s+(.*$)/gm, (match, p1) => {
            let icon = '🩺'; // Default
            for (let key in headerIcons) {
                if (p1.includes(key)) {
                    icon = headerIcons[key];
                    break;
                }
            }
            return `<div class="chat-header">${icon} ${p1}</div>`;
        })
        .replace(/\n\n/g, '<div class="spacing"></div>')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="highlight">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\[(.*?)\]\s*\((.*?)\)/gs, '<a href="$2" target="_blank" class="chat-link">$1 <i class="fas fa-external-link-alt"></i></a>');

    if (role === 'ai') {
        msgDiv.innerHTML = `
            <img src="logo.png" alt="Avatar" class="avatar">
            <div class="message-content">${formattedText}</div>
        `;
    } else {
        let imageHtml = imageUrl ? `<img src="${imageUrl}" class="chat-image-content">` : '';
        msgDiv.innerHTML = `<div class="message-content">${imageHtml}${formattedText}</div>`;
    }

    chatWindow.appendChild(msgDiv);
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
