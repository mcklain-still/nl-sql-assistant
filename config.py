import os
from dotenv import load_dotenv

load_dotenv()

# --- Flask ---
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

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
Table: employees  id, name, email, position, salary, hire_date
Table: suppliers  id, name, contact_email, city
Table: products  id, name, category, price, stock, supplier_id (links to suppliers.id)
Table: customers  id, name, email, city
Table: sales  id, product_id (links to products.id), customer_id (links to customers.id), employee_id (links to employees.id), quantity, sale_date
Table: reviews  id, product_id (links to products.id), customer_id (links to customers.id), rating (1-5), comment, review_date

Relationships:
products.supplier_id = suppliers.id
sales.product_id = products.id
sales.customer_id = customers.id
sales.employee_id = employees.id
reviews.product_id = products.id
reviews.customer_id = customers.id

How to calculate total spent by a customer:
SELECT customers.name, SUM(products.price * sales.quantity) as total_spent
FROM customers
JOIN sales ON customers.id = sales.customer_id
JOIN products ON sales.product_id = products.id
GROUP BY customers.id, customers.name
ORDER BY total_spent DESC

How to get average rating per product:
SELECT products.name, AVG(reviews.rating) as avg_rating
FROM products
JOIN reviews ON products.id = reviews.product_id
GROUP BY products.id, products.name
ORDER BY avg_rating DESC

How to get total sales per employee:
SELECT employees.name, COUNT(sales.id) as total_sales, SUM(products.price * sales.quantity) as revenue_generated
FROM employees
JOIN sales ON employees.id = sales.employee_id
JOIN products ON sales.product_id = products.id
GROUP BY employees.id, employees.name
ORDER BY revenue_generated DESC

Always JOIN all relevant tables when calculating money, revenue, or ratings.
Always alias calculated columns with AS.
"""

# --- Exit commands ---
EXIT_COMMANDS = ["quit", "exit", "bye", "q"]

# --- Validation ---
FORBIDDEN_KEYWORDS = {"DELETE", "DROP", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE"}