import os
from flask import Flask, render_template, request, jsonify, session
from chat_engine import process_message
from config import SECRET_KEY
from utils import log_error, RateLimiter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Rate limiter: 20 requests per minute per IP
rate_limiter = RateLimiter(max_requests=20, window_seconds=60)


@app.route("/health")
def health():
    """Health check endpoint for Render monitoring."""
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    session["chat_history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Rate limiting check
    client_ip = request.remote_addr or "unknown"
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return jsonify({"response": "Too many requests. Please wait a moment before sending another message."}), 429

    chat_history = session.get("chat_history", [])

    try:
        response_text, success, question_type = process_message(user_input, chat_history)

        if not success:
            return jsonify({"response": response_text})

        # Keep only the last 3 exchanges (6 messages) for context
        # without exceeding token limits
        chat_history = chat_history[-6:]
        session["chat_history"] = chat_history

        return jsonify({"response": response_text})

    except Exception as e:
        log_error("Unexpected error in chat endpoint", e)
        return jsonify({"response": "An unexpected error occurred. Please try again."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)