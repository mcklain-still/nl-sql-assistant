import logging
from config import FORBIDDEN_KEYWORDS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate generated SQL for safety.
    
    Args:
        sql: SQL query string to validate
        
    Returns:
        tuple: (is_valid, message)
    """
    sql_upper = sql.upper().strip()
    
    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            logger.warning(f"Forbidden SQL keyword detected: {keyword}")
            return False, f"SQL contains forbidden keyword: {keyword}"
    
    # Check if it's a SELECT statement
    if not sql_upper.startswith("SELECT"):
        logger.warning(f"SQL does not start with SELECT: {sql[:50]}")
        return False, "Only SELECT statements are allowed"
    
    # Check for comment injection
    if "--" in sql or "/*" in sql:
        logger.warning("SQL comment syntax detected")
        return False, "SQL comments are not allowed"
    
    logger.info(f"SQL validation passed: {sql[:50]}...")
    return True, ""


def format_results(columns: list, results: list) -> str:
    """
    Format query results into a readable string.
    
    Args:
        columns: Column names
        results: Query results
        
    Returns:
        Formatted results string
    """
    if not results:
        return "No results found."
    
    header = " | ".join(columns)
    divider = "-" * len(header)
    rows = [" | ".join(str(val) for val in row) for row in results]
    
    return f"{header}\n{divider}\n" + "\n".join(rows)


def log_error(context: str, error: Exception):
    """Log error with context."""
    logger.error(f"{context}: {str(error)}")
