# AI Chatbot for valcobaby.com.au

This project contains the backend and frontend for an AI-powered chatbot designed for valcobaby.com.au. It uses Flask for the backend and simple HTML, CSS, and JavaScript for the frontend. The chatbot is intended to be connected to OpenAI's ChatGPT API.

**Current Status:** The backend API is functional with mocked responses. The frontend UI is built and communicates with this mock backend. The actual OpenAI API call is commented out and needs to be enabled with a valid API key.

## Setup

1.  **Clone the repository (if applicable).**
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Copy `.env.example` to a new file named `.env`:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and add your actual OpenAI API key:
    ```
    OPENAI_API_KEY="sk-yourActualOpenAIapiKeyGoesHere"
    ```

## Running the Development Server

```bash
python app.py
```

The Flask development server will start, typically on `http://127.0.0.1:5000`.
Open this address in your web browser to interact with the chatbot.

## Project Structure

-   `app.py`: The main Flask application. Handles routing, API logic, and serving the frontend.
-   `requirements.txt`: Python dependencies.
-   `.env.example`: Example file for environment variables (especially `OPENAI_API_KEY`).
-   `templates/`: Contains HTML templates.
    -   `index.html`: The main HTML page for the chatbot interface.
-   `static/`: Contains static files.
    -   `style.css`: CSS styles for the chatbot.
    -   `script.js`: JavaScript for frontend logic (sending messages, displaying responses).
-   `README.md`: This file.

## How it Works

1.  The user visits the root URL (`/`), and Flask serves `templates/index.html`.
2.  `static/script.js` handles the chat interface. When the user sends a message:
    a.  It makes an asynchronous `POST` request to the `/api/chat` endpoint on the Flask backend.
    b.  The request body is a JSON object: `{"message": "user's message"}`.
3.  The Flask backend (`app.py`) receives the message at the `/api/chat` route:
    a.  Currently, it uses simulated logic to generate a response based on keywords.
    b.  **(This is the primary place for OpenAI integration)** This is where the call to the OpenAI API should be made.
    c.  It returns a JSON response: `{"response": "chatbot's answer"}`.
4.  The frontend JavaScript receives the response and displays it in the chat window.

## Connecting to OpenAI GPT API

To enable real AI responses:

1.  **Install Libraries:**
    Uncomment `openai` and `python-dotenv` in `requirements.txt`:
    ```
    Flask>=2.0
    openai
    python-dotenv
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Add API Key:**
    Ensure your `OPENAI_API_KEY` is correctly set in your `.env` file (which you should create by copying `.env.example`). This key should be kept private.

3.  **Modify `app.py`:**
    a.  Uncomment the `openai` and `load_dotenv` import lines at the top of `app.py`:
        ```python
        from dotenv import load_dotenv
        import openai
        ```
    b.  Uncomment the `load_dotenv()` call near the top:
        ```python
        load_dotenv()
        ```
    c.  Uncomment the OpenAI API key configuration lines:
        ```python
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            # Consider how to handle this in production (e.g., prevent app start)
        ```
    d.  In the `chat()` function, **replace the simulated response logic** with the actual OpenAI API call. The commented-out section in `app.py` provides a direct template:
        ```python
        # # This is where you would typically call the OpenAI API:
        # response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo", # Or your preferred model, e.g., "gpt-4"
        # messages=[
        # {"role": "system", "content": "You are a helpful assistant for valcobaby.com.au. Answer questions related to Valco Baby products, policies, and general information about the company. Be friendly and concise."},
        # # For more advanced context, you might add conversation history here
        # {"role": "user", "content": user_message}
        # ]
        # )
        # bot_response = response.choices[0].message.content.strip()
        ```
        Ensure you assign the result to `bot_response`.

## Customizing the Chatbot

*   **System Prompt:** The most crucial customization is the `"system"` message content in the OpenAI API call within `app.py`. This message guides the AI's persona, its knowledge boundaries, and its response style. Tailor it carefully to `valcobaby.com.au`.
*   **Frontend Appearance:** Modify `static/style.css` for visual changes and `templates/index.html` for structural changes to the chat interface.
*   **Initial Greeting:** The default greeting message is hardcoded in `templates/index.html`. This can be changed directly or made dynamic.
*   **Valco Baby Specific Knowledge (Advanced):**
    *   For highly accurate and detailed answers about specific Valco Baby products or policies, the "system" prompt might not be enough if the information isn't publicly available for the AI to have learned.
    *   Consider implementing **Retrieval Augmented Generation (RAG)**:
        1.  Store your product information, FAQs, and policy documents in a structured format (e.g., a simple database, JSON files, or Markdown files).
        2.  When a user asks a question, your backend first searches this local knowledge base for relevant information.
        3.  This retrieved information is then passed as additional context (along with the user's question and system prompt) to the OpenAI API. This significantly helps the AI provide accurate, up-to-date, and site-specific answers. This is a more advanced implementation requiring additional logic for searching and context injection.

## Deployment

Refer to the conceptual deployment plan discussed in step 5 of the development plan. Key considerations:
*   Use a production-grade WSGI server (e.g., Gunicorn, Waitress).
*   Manage the `OPENAI_API_KEY` and other sensitive data as secure environment variables in your hosting platform.
*   Choose a suitable hosting platform (PaaS like Heroku, PythonAnywhere, or a VPS).
*   If integrating into an existing `valcobaby.com.au` site that's hosted separately from the chatbot API, ensure CORS (Cross-Origin Resource Sharing) is correctly configured on the Flask backend (e.g., using the `Flask-CORS` extension).

## Further Development Ideas

*   **Conversation History:** Implement sending a summary or the last few turns of the conversation to the OpenAI API. This gives the AI context for follow-up questions. The `messages` array in the OpenAI API call is designed for this.
*   **Streaming Responses:** For a better user experience with potentially longer AI responses, implement response streaming so text appears token by token.
*   **Enhanced Error Handling:** Improve error messages and resilience on both frontend and backend.
*   **User Feedback Mechanism:** Add "thumbs up/down" or a feedback form for responses.
*   **Admin Interface:** A simple interface to manage FAQs (if using RAG), review anonymized chat logs (important: consider privacy implications), or update configurations.
*   **Vector Database for RAG:** For more sophisticated RAG, use a vector database (e.g., Pinecone, Weaviate, FAISS) to store and search your company's knowledge base using semantic search.
*   **Rate Limiting & Security:** Implement rate limiting on the API endpoint to prevent abuse. Further sanitize inputs.
