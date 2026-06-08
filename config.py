import os
import re
from dotenv import load_dotenv

load_dotenv()

# --- Database Config ---
# Railway provides a DATABASE_URL like: mysql://user:password@host:port/dbname
# We support both that and individual env vars for local dev.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Parse Railway-style MySQL connection string: mysql://user:pass@host:port/dbname
    match = re.match(
        r"mysql://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<dbname>.+)",
        DATABASE_URL,
    )
    if match:
        DB_HOST = match.group("host")
        DB_USER = match.group("user")
        DB_PASSWORD = match.group("password")
        DB_NAME = match.group("dbname")
        DB_PORT = int(match.group("port"))
    else:
        raise ValueError("DATABASE_URL format not recognized. Expected: mysql://user:pass@host:port/dbname")
else:
    # Local dev: use individual env vars from .env
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "shopbot_db")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))

# --- OpenAI Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"

# --- Database Schema ---
DATABASE_SCHEMA = """
Table: products  id, name, category, price, stock
Table: customers  id, name, email, city
Table: sales  id, product_id (links to products.id), customer_id (links to customers.id), quantity, sale_date

Relationships:
sales.product_id = products.id
sales.customer_id = customers.id

How to calculate total spent by a customer:
SELECT customers.name, SUM(products.price * sales.quantity) as total_spent
FROM customers
JOIN sales ON customers.id = sales.customer_id
JOIN products ON sales.product_id = products.id
GROUP BY customers.id, customers.name
ORDER BY total_spent DESC

Always JOIN all three tables when calculating money or revenue.
Always alias calculated columns with AS.
"""

# --- Exit commands ---
EXIT_COMMANDS = ["quit", "exit", "bye", "q"]

# --- Validation ---
ALLOWED_SQL_KEYWORDS = {"SELECT", "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER", "ON", "AND", "OR", "GROUP", "BY", "ORDER", "LIMIT", "SUM", "COUNT", "AVG", "MAX", "MIN", "DISTINCT"}
FORBIDDEN_KEYWORDS = {"DELETE", "DROP", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE"}