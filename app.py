import os
from flask import Flask, render_template, request, jsonify, session
from sql_generator import generate_sql, classify_question, generate_business_answer
from answer_generator import generate_answer
from db import run_query
from utils import log_error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "shopbot_secret_key"


@app.route("/")
def index():
    session["data_history"] = []
    session["business_history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Separate histories for data and business questions
    data_history = session.get("data_history", [])
    business_history = session.get("business_history", [])

    try:
        question_type = classify_question(user_input)

        if question_type == "business":
            answer, success, error = generate_business_answer(user_input, business_history)
            if not success:
                return jsonify({"response": f"Sorry, something went wrong: {error}"})

            # Save to business history only
            business_history.append({"role": "user", "content": user_input})
            business_history.append({"role": "assistant", "content": answer})
            session["business_history"] = business_history

        else:
            sql, sql_success, sql_error = generate_sql(user_input, data_history)
            attempts = 0
            while not sql_success and sql == "INVALID" and attempts < 3:
                logger.info(f"Retrying SQL generation... attempt {attempts + 1}")
                sql, sql_success, sql_error = generate_sql(user_input, data_history)
                attempts += 1
                

            if not sql_success:
                if sql == "INVALID":
                    return jsonify({"response": "Sorry, I can only answer questions about the store."})
                return jsonify({"response": "I had trouble understanding that question. Could you try rephrasing it?"})

            columns, results, db_success, db_error = run_query(sql)

            if not db_success:
                return jsonify({"response": f"Sorry, something went wrong: {db_error}"})

            answer, answer_success, answer_error = generate_answer(
                user_question=user_input,
                columns=columns,
                results=results,
                chat_history=data_history
            )

            if not answer_success:
                return jsonify({"response": f"Sorry, something went wrong: {answer_error}"})

            # Save to data history — keep only last 2 exchanges (4 messages) to avoid confusing GPT
            data_history.append({"role": "user", "content": user_input})
            data_history.append({"role": "assistant", "content": f"SQL query was executed successfully. Raw data: {results}"})

            # Keep only the last exchange (2 messages) to prevent GPT confusion
            data_history = data_history[-2:]

            session["data_history"] = data_history

        return jsonify({"response": answer})

    except Exception as e:
        log_error("Unexpected error in chat endpoint", e)
        return jsonify({"response": "An unexpected error occurred. Please try again."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
