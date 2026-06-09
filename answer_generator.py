from openai import OpenAI
import logging
from config import OPENAI_API_KEY, MODEL
from utils import log_error

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(user_question: str, columns: list, results: list, chat_history: None | list = None) -> tuple[str, bool, str]:
    """
    Generate natural language answer from query results.

    Args:
        user_question: Original user question
        columns: Column names from query
        results: Query results
        chat_history: Previous messages in the conversation

    Returns:
        tuple: (answer, success, error_message)
    """
    if chat_history is None:
        chat_history = []

    try:
        logger.info("Generating natural language answer...")

        if not results:
            return "I couldn't find any matching records for your question. This might mean the data doesn't exist in our database, or you could try rephrasing your question.", True, ""

        # Start with the system prompt
        messages = [
            {
                "role": "system",
                "content": "You are a database assistant. Answer questions using any tables available in the database schema. If the information exists in the schema, generate SQL. Only refuse if the information cannot be derived from the database."
            }
        ]

        # Add conversation history so the bot remembers previous messages
        messages.extend(chat_history)

        # Add the current question and results
        messages.append({
            "role": "user",
            "content": f"""Question: {user_question}
Columns: {columns}
Results: {results}
Answer the question naturally based on these results. Format numbers nicely and provide a clear, helpful response."""
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = response.choices[0].message.content.strip()
        logger.info("Answer generated successfully")
        return answer, True, ""

    except Exception as e:
        error_msg = f"Error generating answer: {str(e)}"
        log_error("Answer Generation", e)
        return "", False, error_msg