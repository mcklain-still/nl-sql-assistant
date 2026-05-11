import mysql.connector
import logging
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Create and return a MySQL database connection.
    
    Returns:
        mysql.connector.MySQLConnection
        
    Raises:
        mysql.connector.Error: If connection fails
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        logger.info("Database connection established")
        return conn
    except mysql.connector.Error as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise


def run_query(sql: str) -> tuple[list, list, bool, str]:
    """
    Execute a SQL query and return results.
    
    Args:
        sql: SQL query to execute
        
    Returns:
        tuple: (columns, results, success, error_message)
              - success: bool indicating if query executed successfully
              - error_message: error message if failed
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        logger.info(f"Executing query: {sql[:100]}...")
        cursor.execute(sql)
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        logger.info(f"Query successful, returned {len(results)} rows")
        return columns, results, True, ""
        
    except mysql.connector.Error as e:
        error_msg = f"Database error: {str(e)}"
        logger.error(error_msg)
        return None, None, False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return None, None, False, error_msg
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logger.info("Database connection closed")
