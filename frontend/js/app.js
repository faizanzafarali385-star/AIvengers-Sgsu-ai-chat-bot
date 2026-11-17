// SGSU Chatbot Frontend Script

// Dynamically determine the backend API URL:
// - If served directly from FastAPI (port 8000 or production domain), use the current origin
// - If served from a separate dev server (e.g., port 8080, port 5501) or file://, target http://localhost:8000
const API_URL = (window.location.protocol.startsWith('http') && (window.location.port === '8000' || window.location.port === ''))
    ? window.location.origin
    : 'http://localhost:8000';

const messagesArea = document.getElementById('messagesArea');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const darkModeToggle = document.getElementById('darkModeToggle');
let isConnected = false;

// Dark Mode Toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
    updateDarkModeIcon();
}

function updateDarkModeIcon() {
    const isDarkMode = document.body.classList.contains('dark-mode');
    if (darkModeToggle) {
        darkModeToggle.textContent = isDarkMode ? '☀️' : '🌙';
    }
}

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
}

// Update icon on load
window.addEventListener('load', () => {
    updateDarkModeIcon();
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }
});

// Check API connection on page load
async function checkApiConnection() {
    try {
        const response = await fetch(`${API_URL}/health`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        isConnected = response.ok;
        if (!isConnected) {
            showConnectionError();
        }
    } catch (error) {
        isConnected = false;
        showConnectionError();
    }
}

function showConnectionError() {
    // Prevent duplicate error banners
    if (document.getElementById('connection-error-banner')) return;

    const errorDiv = document.createElement('div');
    errorDiv.id = 'connection-error-banner';
    errorDiv.style.cssText = 'background: #ffebee; color: #c62828; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 13px; border-left: 4px solid #c62828;';
    errorDiv.innerHTML = '<strong>⚠️ Backend Connection Error</strong><br>Make sure the backend is running on ' + API_URL + '<br><button onclick="checkApiConnection(); this.parentElement.remove();" style="margin-top: 8px; padding: 6px 12px; background: #c62828; color: white; border: none; border-radius: 4px; cursor: pointer;">Retry</button>';
    messagesArea.insertBefore(errorDiv, messagesArea.firstChild);
}

// Check connection on page load
window.addEventListener('load', checkApiConnection);

// Focus input on load
if (questionInput) {
    questionInput.focus();

    // Send message on Enter key
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Send message on button click
if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
}

// Clear chat
if (clearBtn) {
    clearBtn.addEventListener('click', clearChat);
}

function selectSuggestion(text) {
    if (questionInput) {
        questionInput.value = text;
        sendMessage();
    }
}

async function sendMessage() {
    const question = questionInput.value.trim();
    
    if (!question) return;

    // Check connection first
    if (!isConnected) {
        addMessage('Please wait for the connection to be established. Retrying...', 'error');
        setTimeout(checkApiConnection, 1000);
        return;
    }

    // Clear input
    questionInput.value = '';
    questionInput.focus();

    // Add user message to UI
    addMessage(question, 'user');

    // Show typing indicator
    const typingId = showTypingIndicator();

    try {
        // Send request to backend with timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout

        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (!response.ok) {
            if (response.status === 500) {
                throw new Error('Backend error: ' + response.statusText);
            } else if (response.status === 400) {
                throw new Error('Invalid request');
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        }

        const data = await response.json();

        // Add bot response
        addMessage(data.answer, 'bot', data.confidence);
        isConnected = true;

    } catch (error) {
        // Remove typing indicator
        removeTypingIndicator(typingId);

        // Show error message with helpful instructions
        let errorMsg = '';
        if (error.name === 'AbortError') {
            errorMsg = '⏱️ Request timeout. Backend might be slow. Please try again.';
        } else if (error.message && error.message.includes('Failed to fetch')) {
            errorMsg = '🔗 Connection failed. Make sure:\n1. Backend is running (python main.py)\n2. Backend is on http://localhost:8000\n3. Firewall is not blocking the connection\n\nTry again in a moment...';
            isConnected = false;
            // Auto-retry connection after 3 seconds
            setTimeout(checkApiConnection, 3000);
        } else if (error.message) {
            errorMsg = `❌ Error: ${error.message}`;
        } else {
            errorMsg = '❌ Unknown error occurred. Please try again.';
        }
        addMessage(errorMsg, 'error');
        console.error('Full error:', error);
    }

    // Scroll to bottom
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function formatBotMessage(text) {
    if (!text) return '';
    
    // Escape HTML special characters
    let safe = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Convert **bold** to <strong>
    safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Convert URLs into clickable anchor tags
    safe = safe.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');

    return safe;
}

function addMessage(text, type = 'bot', confidence = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    // Create logo section
    const logoDiv = document.createElement('div');
    logoDiv.className = 'message-logo';

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'logo-avatar';
    
    const labelDiv = document.createElement('div');
    labelDiv.className = 'logo-label';

    if (type === 'user') {
        avatarDiv.textContent = '👤';
        labelDiv.textContent = 'You';
    } else if (type === 'bot') {
        avatarDiv.textContent = '🤖';
        labelDiv.textContent = 'Bot';
    } else {
        avatarDiv.textContent = '⚠️';
        labelDiv.textContent = 'Error';
    }

    logoDiv.appendChild(avatarDiv);
    logoDiv.appendChild(labelDiv);

    // Create content wrapper
    const wrapperDiv = document.createElement('div');
    wrapperDiv.className = 'message-wrapper';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (type === 'bot') {
        contentDiv.innerHTML = formatBotMessage(text);
    } else {
        contentDiv.textContent = text;
    }

    if (type === 'bot' && confidence !== null && confidence > 0) {
        const confidenceDiv = document.createElement('div');
        confidenceDiv.className = 'confidence-badge';
        confidenceDiv.textContent = `Confidence: ${(confidence * 100).toFixed(0)}%`;
        contentDiv.appendChild(document.createElement('br'));
        contentDiv.appendChild(confidenceDiv);
    }

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    wrapperDiv.appendChild(contentDiv);
    wrapperDiv.appendChild(timeDiv);

    if (type === 'user') {
        messageDiv.appendChild(wrapperDiv);
        messageDiv.appendChild(logoDiv);
    } else {
        messageDiv.appendChild(logoDiv);
        messageDiv.appendChild(wrapperDiv);
    }

    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function showTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.id = 'typing-indicator';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

    contentDiv.appendChild(typingDiv);
    messageDiv.appendChild(contentDiv);
    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;

    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function clearChat() {
    messagesArea.innerHTML = `
        <div class="welcome-message">
            <p><strong>Welcome to the Chatbot!</strong></p>
            <p style="margin-top: 8px; font-size: 13px;">Ask me anything about Scope Global Skill University, Get detailed course information 🎓</p>
        </div>
        <div class="suggestions-container">
            <button class="suggestion-btn" onclick="selectSuggestion('Tell me about SGSU')">About SGSU</button>
            <button class="suggestion-btn" onclick="selectSuggestion('What are the admission requirements?')">Admission</button>
            <button class="suggestion-btn" onclick="selectSuggestion('Tell me about the programs and courses')">Programs</button>
            <button class="suggestion-btn" onclick="selectSuggestion('What are the placement opportunities?')">Placements</button>
        </div>
    `;
}
