from openai import OpenAI
import logging
from config import OPENAI_API_KEY, MODEL
from utils import log_error

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(user_question: str, columns: list, results: list) -> tuple[str, bool, str]:
    """
    Generate natural language answer from query results.
    
    Args:
        user_question: Original user question
        columns: Column names from query
        results: Query results
        
    Returns:
        tuple: (answer, success, error_message)
    """
    try:
        logger.info("Generating natural language answer...")
        
        if not results:
            return "No results found for your question.", True, ""
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful store assistant. Answer the user's question naturally based on the database results. Be concise and friendly. Avoid listing raw data; provide insights instead."
                },
                {
                    "role": "user",
                    "content": f"""Question: {user_question}
Columns: {columns}
Results: {results}

Answer the question naturally based on these results. Format numbers nicely and provide a clear, helpful response."""
                }
            ]
        )
        
        answer = response.choices[0].message.content.strip()
        logger.info("Answer generated successfully")
        return answer, True, ""
        
    except Exception as e:
        error_msg = f"Error generating answer: {str(e)}"
        log_error("Answer Generation", e)
        return "", False, error_msg
