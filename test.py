# ShopBot — AI-powered store database chatbot
# Converts plain English questions into SQL queries and returns natural language answers

from openai import OpenAI
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def generate_sql(user_question):
    schema = """
    Table: products  — id, name, category, price, stock
    Table: customers — id, name, email, city
    Table: sales     — id, product_id (links to products.id), customer_id (links to customers.id), quantity, sale_date

    Relationships:
    - sales.product_id = products.id
    - sales.customer_id = customers.id
    - Total spent = products.price * sales.quantity
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""You are a SQL expert. Convert the user's question into a valid MySQL query.
                Database schema: {schema}
                Rules:
                - Return ONLY the SQL query, no explanation, no markdown
                - Only use SELECT statements, never DELETE or DROP
                - If the question cannot be answered with this schema, return: INVALID"""
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    return response.choices[0].message.content.strip()


def run_query(sql):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()  # always close to free resources
        conn.close()
        return columns, results

    except Exception as e:
        return None, str(e)


def generate_answer(user_question, columns, results):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful store assistant. Answer the user's question naturally based on the database results. Be concise and friendly."
            },
            {
                "role": "user",
                "content": f"""Question: {user_question}
                Columns: {columns}
                Results: {results}
                Answer the question naturally based on these results."""
            }
        ]
    )

    return response.choices[0].message.content.strip()


def main():
    print("================================")
    print("         ShopBot 🛍️            ")
    print("  Ask me anything about the store!")
    print("  Type 'quit' to exit")
    print("================================\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("ShopBot: Goodbye! 👋")
            break

        sql = generate_sql(user_input)

        if sql == "INVALID":
            print("ShopBot: Sorry, I can only answer questions about the store.\n")
            continue

        columns, results = run_query(sql)

        if columns is None:
            print(f"ShopBot: Sorry, something went wrong — {results}\n")
            continue

        answer = generate_answer(user_question=user_input, columns=columns, results=results)
        print(f"ShopBot: {answer}\n")


if __name__ == "__main__":
    main()