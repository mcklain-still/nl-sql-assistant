import os
from flask import Flask, render_template, request, jsonify, session
from chat_engine import process_message
from utils import log_error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "shopbot_secret_key"


@app.route("/")
def index():
    session["chat_history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    chat_history = session.get("chat_history", [])

    try:
        response_text, success, question_type = process_message(user_input, chat_history)

        if not success:
            return jsonify({"response": response_text})

        # Keep only the last exchange to prevent GPT confusion
        chat_history = chat_history[-2:]
        session["chat_history"] = chat_history

        return jsonify({"response": response_text})

    except Exception as e:
        log_error("Unexpected error in chat endpoint", e)
        return jsonify({"response": "An unexpected error occurred. Please try again."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)