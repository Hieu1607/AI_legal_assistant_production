document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatBox = document.getElementById('chat-box');

    const API_ENDPOINT = 'https://ai-legal-assistant-8g4g.onrender.com/rag/';

    const sendMessage = async () => {
        const question = userInput.value.trim();
        if (question === '') return;

        displayMessage(question, 'user');
        userInput.value = '';
        userInput.style.height = 'auto'; // Reset height

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
            
            if (result.status === 'success' && result.data && result.data.answer) {
                displayMessage(result.data.answer, 'bot');
            } else {
                displayMessage('Sorry, I could not find an answer.', 'bot');
            }

        } catch (error) {
            console.error('Failed to fetch from API:', error);
            displayMessage('There was an error connecting to the assistant. Please try again later.', 'bot');
        }
    };

    const displayMessage = (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
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