from openai import OpenAI
import logging
from config import OPENAI_API_KEY, MODEL, DATABASE_SCHEMA
from utils import validate_sql, log_error

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def classify_question(user_question: str) -> str:
    """
    Detect whether the question needs database data or business advice.

    Returns either "data" or "business"
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """Classify the user's question into one of two categories:
"data" — questions that need database information to answer
Examples: "what is our best selling product", "who spent the most", "how many items in stock"

"business" — questions asking for advice, strategy, or growth recommendations
Examples: "how should we grow sales", "what marketing strategy should we use", "should we expand our product range"

Reply with ONLY one word: data or business"""
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )
    result = response.choices[0].message.content.strip().lower()
    logger.info(f"Question classified as: {result}")
    return result if result in ["data", "business"] else "data"


def generate_business_answer(user_question: str, chat_history: list = []) -> tuple[str, bool, str]:
    """
    Answer a business strategy question using store context and GPT knowledge.

    Returns:
        tuple: (answer, success, error_message)
    """
    try:
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful business advisor for a small retail store.
The store sells the following types of products: Electronics, Footwear, Fitness gear, and Accessories.
You have access to the store's data context from previous answers in the conversation.
Give practical, specific advice based on what you know about the store.
Be concise, friendly, and actionable. Use bullet points where helpful."""
            }
        ]

        # Add conversation history for context
        messages.extend(chat_history)

        messages.append({"role": "user", "content": user_question})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = response.choices[0].message.content.strip()
        logger.info("Business answer generated successfully")
        return answer, True, ""

    except Exception as e:
        log_error("Business answer generation failed", e)
        return "", False, str(e)


def generate_sql(user_question: str, chat_history: list = []) -> tuple[str, bool, str]:
    """
    Generate SQL from natural language question using OpenAI.

    Args:
        user_question: Natural language question
        chat_history: Previous messages in the conversation

    Returns:
        tuple: (sql_query, success, error_message)
    """
    try:
        logger.info(f"Generating SQL for question: {user_question[:50]}...")

        messages = [
            {
                "role": "system",
                "content": f"""You are a SQL expert. Your ONLY job is to return a valid MySQL SELECT statement. Nothing else.

Database schema:
{DATABASE_SCHEMA}

Rules:
- Your response must be a single SQL query starting with SELECT
- No explanations, no markdown, no natural language, no introductions
- Only use SELECT statements, never DELETE or DROP
- Pronouns like "she", "he", "they", "her", "him", "their" always refer to the most recently mentioned person in the conversation history
- When you see a pronoun, look back through the conversation history, find the most recent person's name, and use that name in the SQL WHERE clause
- For example if history shows "Alice Johnson" and user asks "what city are they from?" write: SELECT city FROM customers WHERE name = 'Alice Johnson'
- If the question is a follow up referencing a previous answer, use the conversation history to resolve who "they" refers to and write the appropriate SQL
- If the question cannot be answered with this schema AND has no relation to previous conversation, return: INVALID

Example of correct response:
User: what does Alice Johnson buy?
You: SELECT products.name FROM products JOIN sales ON products.id = sales.product_id JOIN customers ON sales.customer_id = customers.id WHERE customers.name = 'Alice Johnson'

Example of WRONG response:
User: what does she buy?
You: Alice Johnson buys the following products..."""
            }
        ]

        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_question})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        sql = response.choices[0].message.content.strip()

        if sql == "INVALID":
            logger.info("Question deemed outside schema scope")
            return "INVALID", False, "Question is outside the scope of available data"

        is_valid, error_msg = validate_sql(sql)
        if not is_valid:
            return "", False, error_msg

        logger.info(f"SQL generated successfully: {sql[:100]}...")
        return sql, True, ""

    except Exception as e:
        error_msg = f"Error generating SQL: {str(e)}"
        log_error("SQL Generation", e)
        return "", False, error_msg