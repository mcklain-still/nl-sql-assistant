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


def generate_business_answer(user_question: str, chat_history: None | list = None) -> tuple[str, bool, str]:
    """
    Answer a business strategy question using store context and GPT knowledge.

    Returns:
        tuple: (answer, success, error_message)
    """
    if chat_history is None:
        chat_history = []

    try:
        messages = [
            {
                "role": "system",
                "content":  """You are a helpful business advisor for a small retail store.
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


def generate_sql(user_question: str, chat_history: None | list = None) -> tuple[str, bool, str]:
    """
    Generate SQL from natural language question using OpenAI.

    Args:
        user_question: Natural language question
        chat_history: Previous messages in the conversation

    Returns:
        tuple: (sql_query, success, error_message)
    """
    if chat_history is None:
        chat_history = []

    try:
        logger.info(f"Generating SQL for question: {user_question[:50]}...")

        messages = [
            {
                "role": "system",
                "content": f"""You are a MySQL expert. Your only job is to write SELECT queries.

                Schema:
                {DATABASE_SCHEMA}

                Rules:
                1. Always respond with ONLY a valid SQL SELECT statement
                2. Never write explanations, markdown, or natural language
                3. Your response must start with SELECT
                4. Use JOINs when needed across tables
                5. Only return INVALID if the question cannot be answered using the database schema provided.
                6. ALWAYS qualify column names with their table name or alias (e.g. employees.salary not just salary) to avoid ambiguous or unknown column errors.
                7. When using subqueries or derived tables, only reference columns that exist in that subquery's result — do not reference outer table columns in ORDER BY of a derived table.
                8. Use aliases for calculated columns and reference those aliases (not raw column names) in ORDER BY.
                If the question is ambiguous or refers to previous context (e.g., "she", "he", "that employee"), attempt to resolve it using chat history.

                Examples of valid questions you MUST answer with SQL:
                - "what is our total revenue" -> SELECT SUM(products.price * sales.quantity) AS total_revenue FROM sales JOIN products ON sales.product_id = products.id
                - "who is our best customer" -> SELECT customers.name, SUM(products.price * sales.quantity) AS total_spent FROM customers JOIN sales ON customers.id = sales.customer_id JOIN products ON sales.product_id = products.id GROUP BY customers.id ORDER BY total_spent DESC LIMIT 1
                - "what is our best selling product" -> SELECT products.name, SUM(sales.quantity) AS total_sold FROM products JOIN sales ON products.id = sales.product_id GROUP BY products.id ORDER BY total_sold DESC LIMIT 1
                - "average salary vs highest earners" -> SELECT employees.name, employees.salary, (SELECT AVG(e.salary) FROM employees e) AS avg_salary FROM employees ORDER BY employees.salary DESC LIMIT 5"""
            }
        ]

        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_question})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        sql = response.choices[0].message.content.strip()

        # Strip markdown code fences if present (GPT sometimes wraps SQL in backticks)
        if sql.startswith("```"):
            sql = sql.strip("`").strip()
            if sql.lower().startswith("sql"):
                sql = sql[3:].strip()

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


def generate_sql_with_correction(
    user_question: str,
    failed_sql: str,
    db_error: str,
    chat_history: None | list = None,
) -> tuple[str, bool, str]:
    """
    Re-generate SQL after a database error, feeding the error back to the LLM
    so it can produce a corrected query.

    Args:
        user_question: The original natural-language question
        failed_sql: The SQL that failed
        db_error: The database error message
        chat_history: Previous conversation messages

    Returns:
        tuple: (sql_query, success, error_message)
    """
    if chat_history is None:
        chat_history = []

    try:
        logger.info(f"Attempting SQL correction for error: {db_error[:100]}")

        messages = [
            {
                "role": "system",
                "content": f"""You are a MySQL expert. Your previous SQL attempt failed and you must fix it.

                Schema:
                {DATABASE_SCHEMA}

                The previously generated SQL was:
                {failed_sql}

                The database returned this error:
                {db_error}

                Rules:
                1. Return ONLY a corrected valid SQL SELECT statement.
                2. Never write explanations, markdown, or natural language.
                3. Your response must start with SELECT.
                4. ALWAYS qualify column names with their table name or alias (e.g. employees.salary not just salary).
                5. When using subqueries or derived tables, only reference columns that exist in that subquery's result.
                6. Use aliases for calculated columns and reference those aliases in ORDER BY.
                7. Ensure all column references are valid for the tables being queried."""
            }
        ]

        messages.extend(chat_history)
        messages.append({
            "role": "user",
            "content": f"Fix the SQL for this question: {user_question}"
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        sql = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        if sql.startswith("```"):
            sql = sql.strip("`").strip()
            if sql.lower().startswith("sql"):
                sql = sql[3:].strip()

        is_valid, error_msg = validate_sql(sql)
        if not is_valid:
            return "", False, error_msg

        logger.info(f"Corrected SQL generated: {sql[:100]}...")
        return sql, True, ""

    except Exception as e:
        error_msg = f"Error generating corrected SQL: {str(e)}"
        log_error("SQL Correction", e)
        return "", False, error_msg
