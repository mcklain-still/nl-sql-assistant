import os
from dotenv import load_dotenv

load_dotenv()

# Database Config
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# OpenAI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"

# Database Schema
DATABASE_SCHEMA = """
Table: products  id, name, category, price, stock
Table: customers  id, name, email, city
Table: sales  id, product_id (links to products.id), customer_id (links to customers.id), quantity, sale_date

Relationships:
sales.product_id = products.id
sales.customer_id = customers.id
Total spent = products.price * sales.quantity
"""

# Exit commands
EXIT_COMMANDS = ["quit", "exit", "bye", "q"]

# Validation
ALLOWED_SQL_KEYWORDS = {"SELECT", "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER", "ON", "AND", "OR", "GROUP", "BY", "ORDER", "LIMIT", "SUM", "COUNT", "AVG", "MAX", "MIN", "DISTINCT"}
FORBIDDEN_KEYWORDS = {"DELETE", "DROP", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE", "EXEC", "EXECUTE"}
