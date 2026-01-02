const chatHistory = document.getElementById('chatHistory');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Initialize: Remove welcome message on first interaction
let isFirstMessage = true;

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;

    // Remove welcome message on first interaction
    if (isFirstMessage) {
        const welcomeMsg = chatHistory.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        isFirstMessage = false;
    }

    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input and disable form
    messageInput.value = '';
    setFormState(false);

    // Show typing indicator
    const typingId = showTypingIndicator();

    try {
        // Call the Flask API
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        // Parse JSON response
        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        // Handle response based on success flag
        if (data.success) {
            addMessage(data.response, 'bot');
        } else {
            // Show error message
            const errorMsg = data.error || 'An error occurred. Please try again.';
            addMessage(`Error: ${errorMsg}`, 'error');
        }

    } catch (error) {
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Handle network or parsing errors
        console.error('Error:', error);
        addMessage('Failed to connect to the server. Please check your connection and try again.', 'error');
    } finally {
        // Re-enable form
        setFormState(true);
        messageInput.focus();
    }
});

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatHistory.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    scrollToBottom();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.id = 'typing-indicator';
    
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'typing-indicator';
    
    indicatorDiv.innerHTML = `
        <span>Assistant is thinking</span>
        <div class="typing-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;
    
    typingDiv.appendChild(indicatorDiv);
    chatHistory.appendChild(typingDiv);
    
    // Auto-scroll to bottom
    scrollToBottom();
    
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const typingElement = document.getElementById(id);
    if (typingElement) {
        typingElement.remove();
    }
}

function scrollToBottom() {
    chatHistory.scrollTo({
        top: chatHistory.scrollHeight,
        behavior: 'smooth'
    });
}

function setFormState(enabled) {
    messageInput.disabled = !enabled;
    sendButton.disabled = !enabled;
}

// Focus input on load
messageInput.focus();