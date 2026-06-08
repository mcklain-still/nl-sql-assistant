import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Config ---
# Render + Aiven: set these env vars in your Render dashboard
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

# --- OpenAI Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

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