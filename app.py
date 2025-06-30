from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import openai
from flask_cors import CORS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                    "You are a helpful assistant for valcobaby.com.au. "
                    "Answer questions about Valco Baby products, policies, and general info. "
                    "Be friendly and concise."
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        bot_response = resp.choices[0].message.content.strip()
        return jsonify({"response": bot_response})
    except Exception as e:
        print(f"OpenAI error: {e}")
        return jsonify({"error": "Failed to get response from AI"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
