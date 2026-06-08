import logging
from config import FORBIDDEN_KEYWORDS

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

    # Check if it starts with a SELECT-like read operation
    # This accepts SELECT and WITH (common table expressions)
    if not any(sql_upper.startswith(kw) for kw in ("SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN")):
        logger.warning(f"SQL does not start with a read-only keyword: {sql[:50]}")
        return False, "Only SELECT statements are allowed"

    # Check for comment injection
    if "--" in sql or "/*" in sql:
        logger.warning("SQL comment syntax detected")
        return False, "SQL comments are not allowed"

    logger.info(f"SQL validation passed: {sql[:50]}...")
    return True, ""


def log_error(context: str, error: Exception):
    """Log error with context."""
    logger.error(f"{context}: {str(error)}")