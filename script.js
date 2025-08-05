document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatBox = document.getElementById('chat-box');

    const API_ENDPOINT = 'https://ai-legal-assistant-8g4g.onrender.com/rag';

    const sendMessage = async () => {
        const question = userInput.value.trim();
        if (question === '') return;

        displayMessage(question, 'user');
        userInput.value = '';
        userInput.style.height = 'auto'; // Reset height

        // Show typing indicator
        const typingElement = showTypingIndicator();

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const result = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator(typingElement);
            
            if (result.status === 'success' && result.data && result.data.answer) {
                await displayTypingMessage(result.data.answer, 'bot');
            } else {
                await displayTypingMessage('Sorry, I could not find an answer.', 'bot');
            }

        } catch (error) {
            console.error('Failed to fetch from API:', error);
            // Remove typing indicator
            removeTypingIndicator(typingElement);
            await displayTypingMessage('There was an error connecting to the assistant. Please try again later.', 'bot');
        }
    };

    const displayMessage = (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    };

    const showTypingIndicator = () => {
        const typingElement = document.createElement('div');
        typingElement.classList.add('message', 'bot-message', 'typing-indicator');
        typingElement.innerHTML = `
            <span class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </span>
            <span class="typing-text">AI đang suy nghĩ...</span>
        `;
        chatBox.appendChild(typingElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return typingElement;
    };

    const removeTypingIndicator = (typingElement) => {
        if (typingElement && typingElement.parentNode) {
            chatBox.removeChild(typingElement);
        }
    };

    const displayTypingMessage = async (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        chatBox.appendChild(messageElement);
        
        // Split message into words for more natural typing effect
        const words = message.split(' ');
        let currentText = '';
        
        for (let i = 0; i < words.length; i++) {
            currentText += (i > 0 ? ' ' : '') + words[i];
            messageElement.textContent = currentText;
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Add delay between words (adjust speed here)
            await new Promise(resolve => setTimeout(resolve, 50));
        }
        
        // Add a cursor effect at the end
        messageElement.innerHTML = currentText + '<span class="typing-cursor">|</span>';
        
        // Remove cursor after a short delay
        setTimeout(() => {
            messageElement.textContent = currentText;
        }, 1000);
    };

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = `${userInput.scrollHeight}px`;
    });
});