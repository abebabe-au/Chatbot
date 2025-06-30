document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatbotContainer = document.getElementById('chatbot-container'); // For scrolling

    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
        
        // Optional: Add sender name (could be configurable)
        // const senderNameElement = document.createElement('div');
        // senderNameElement.classList.add('message-sender');
        // senderNameElement.textContent = sender === 'user' ? 'You' : 'Valco Bot';
        // messageElement.appendChild(senderNameElement);

        const messageTextElement = document.createElement('div');
        messageTextElement.textContent = message;
        messageElement.appendChild(messageTextElement);

        chatWindow.appendChild(messageElement);
        scrollToBottom();
    }

    function scrollToBottom() {
        // Scroll the chat window to the bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('message', 'bot-message', 'typing-indicator');
        typingIndicator.innerHTML = `<span></span><span></span><span></span>`;
        chatWindow.appendChild(typingIndicator);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const typingIndicator = chatWindow.querySelector('.typing-indicator');
        if (typingIndicator) {
            chatWindow.removeChild(typingIndicator);
        }
    }

    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user');
        userInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            });

            removeTypingIndicator();

            if (!response.ok) {
                const errorData = await response.json().catch(() => null); // Try to parse error, but don't fail if no JSON
                const errorMessage = errorData && errorData.error ? errorData.error : `Error: ${response.status} ${response.statusText}`;
                addMessage(`Sorry, I encountered an error: ${errorMessage}`, 'bot');
                console.error('Error sending message:', response.status, response.statusText, errorData);
                return;
            }

            const data = await response.json();
            if (data.response) {
                addMessage(data.response, 'bot');
            } else if (data.error) {
                addMessage(`Error from bot: ${data.error}`, 'bot');
            } else {
                addMessage("Sorry, I didn't get a valid response.", 'bot');
            }

        } catch (error) {
            removeTypingIndicator();
            addMessage('Sorry, I was unable to connect to the chatbot service. Please check your connection or try again later.', 'bot');
            console.error('Network or other error:', error);
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Optional: Add an initial greeting from the bot
    // setTimeout(() => {
    //     addMessage("Hello! I'm the Valco Baby assistant. How can I help you today?", 'bot');
    // }, 500);
});
