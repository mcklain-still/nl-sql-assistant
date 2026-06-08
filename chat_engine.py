"""
Core chat engine — shared logic used by both the web app and CLI.
This prevents duplication between app.py and cli.py.
"""
from typing import Optional
from sql_generator import generate_sql, classify_question, generate_business_answer
from answer_generator import generate_answer
from db import run_query
import logging

logger = logging.getLogger(__name__)


def process_data_question(
    user_input: str,
    chat_history: list
) -> tuple[str, bool]:
    """
    Process a data-oriented question: classify → generate SQL → run query → answer.

    Args:
        user_input: The user's question
        chat_history: Previous conversation messages

    Returns:
        tuple: (response_text, success)
    """
    sql, sql_success, sql_error = generate_sql(user_input, chat_history)

    if not sql_success:
        if sql == "INVALID":
            return "Sorry, I can only answer questions about the store.", True
        return "I had trouble understanding that question. Could you try rephrasing it?", True

    columns, results, db_success, db_error = run_query(sql)

    if not db_success:
        return f"Sorry, something went wrong: {db_error}", True

    answer, answer_success, answer_error = generate_answer(
        user_question=user_input,
        columns=columns,
        results=results,
        chat_history=chat_history
    )

    if not answer_success:
        return f"Sorry, something went wrong: {answer_error}", True

    return answer, True


def process_business_question(
    user_input: str,
    chat_history: list
) -> tuple[str, bool]:
    """
    Process a business advice question directly with GPT.

    Args:
        user_input: The user's question
        chat_history: Previous conversation messages

    Returns:
        tuple: (response_text, success)
    """
    answer, success, error = generate_business_answer(user_input, chat_history)
    if not success:
        return f"Sorry, something went wrong: {error}", False
    return answer, True


def process_message(
    user_input: str,
    chat_history: Optional[list] = None
) -> tuple[str, bool, str]:
    """
    Process a user message and return a response.

    Args:
        user_input: The user's question
        chat_history: Optional conversation history (will be mutated in-place)

    Returns:
        tuple: (response_text, success, question_type)
               question_type is "data" or "business"
    """
    if chat_history is None:
        chat_history = []

    question_type = classify_question(user_input)

    if question_type == "business":
        response, success = process_business_question(user_input, chat_history)
    else:
        response, success = process_data_question(user_input, chat_history)

    if success:
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

    return response, success, question_type