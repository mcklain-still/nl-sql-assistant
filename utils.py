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

    # Check for comment injection — ignore comments inside string literals
    # Remove string literal contents before checking for comment markers
    stripped = ""
    in_string = False
    string_char = None
    for ch in sql:
        if in_string:
            if ch == string_char:
                in_string = False
            continue
        if ch in ("'", '"'):
            in_string = True
            string_char = ch
            continue
        stripped += ch
    if "--" in stripped or "/*" in stripped:
        logger.warning("SQL comment syntax detected")
        return False, "SQL comments are not allowed"

    logger.info(f"SQL validation passed: {sql[:50]}...")
    return True, ""


def log_error(context: str, error: Exception):
    """Log error with context."""
    logger.error(f"{context}: {str(error)}")


class RateLimiter:
    """
    Simple in-memory rate limiter using a sliding window.
    Tracks request counts per client IP.
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clients: dict[str, list[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        """
        Check if a request from client_id is allowed.
        Returns True if under the limit, False if rate-limited.
        """
        import time
        now = time.time()
        cutoff = now - self.window_seconds

        # Get or create entry for this client
        timestamps = self._clients.get(client_id, [])

        # Prune timestamps outside the window
        timestamps = [t for t in timestamps if t > cutoff]

        if len(timestamps) >= self.max_requests:
            self._clients[client_id] = timestamps
            return False

        timestamps.append(now)
        self._clients[client_id] = timestamps
        return True
