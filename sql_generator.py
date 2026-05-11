from openai import OpenAI
import logging
from config import OPENAI_API_KEY, MODEL, DATABASE_SCHEMA
from utils import validate_sql, log_error

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_sql(user_question: str) -> tuple[str, bool, str]:
    """
    Generate SQL from natural language question using OpenAI.
    
    Args:
        user_question: Natural language question
        
    Returns:
        tuple: (sql_query, success, error_message)
    """
    try:
        logger.info(f"Generating SQL for question: {user_question[:50]}...")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a SQL expert. Convert the user's question into a valid MySQL query.
Database schema:
{DATABASE_SCHEMA}

Rules:
- Return ONLY the SQL query, no explanation, no markdown
- Only use SELECT statements, never DELETE or DROP
- If the question cannot be answered with this schema, return: INVALID
- Write queries that are safe and efficient"""
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ]
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
