from flask import Flask, request, jsonify, render_template # Added render_template
import os
# We'll use dotenv to load the OpenAI API key from a .env file
# from dotenv import load_dotenv
# import openai

# load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static') # Specified template and static folders

# Configure the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# In a real scenario, you would validate this key or use a more secure way to store/access it.
# For now, we'll assume it's set in the environment.
# if not openai.api_key:
#     print("Error: OPENAI_API_KEY environment variable not set.")
    # In a production app, you might want to exit or handle this more gracefully.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # MOVED: Actual OpenAI call will be added later.
        # For now, let's simulate a response.
        # This is where you would typically call the OpenAI API:
        # response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo", # Or your preferred model
        # messages=[
        # {"role": "system", "content": "You are a helpful assistant for valcobaby.com.au."},
        # {"role": "user", "content": user_message}
        # ]
        # )
        # bot_response = response.choices[0].message.content.strip()

        # Simulate a bot response for now
        if "hello" in user_message.lower():
            bot_response = "Hello! How can I help you today with Valco Baby products?"
        elif "pram" in user_message.lower():
            bot_response = "We have a wide range of prams. Are you looking for something specific, like a lightweight model or one for twins?"
        else:
            bot_response = "Thanks for your message. I'm still under development, but I'll soon be able to help with all your Valco Baby questions!"

        return jsonify({"response": bot_response})

    except Exception as e:
        # In a real app, log the error e
        print(f"Error processing chat: {e}")
        return jsonify({"error": "Failed to get response from AI"}), 500

if __name__ == '__main__':
    # In a production environment, use a WSGI server like Gunicorn or Waitress
    app.run(debug=True, port=5000)
