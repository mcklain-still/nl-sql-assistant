# Store Analytics Assistant

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46BC99?style=for-the-badge&logo=render&logoColor=white)](https://nl-sql-assistant.onrender.com)

A natural language interface for relational database querying, powered by
OpenAI and MySQL. Converts plain English questions into validated SQL queries
and returns human-readable answers through a web-based chat interface.

## Live Demo

Try it now:
**[nl-sql-assistant.onrender.com](https://nl-sql-assistant.onrender.com)**

Ask questions like:

- *What is our best selling product?*
- *Who is our best customer?*
- *How can we grow our sales?*

---

## Overview

This project demonstrates an end-to-end AI-driven query layer that bridges
conversational AI and structured data. It was built to showcase practical
skills in prompt engineering, database design, API integration, and full stack
Python development.

## Architecture

```text
User Question
       |
Question Classifier (data vs. business)
       |                    |
SQL Generator         Business Advisor
       |                    |
SQL Validator         GPT Response
       |
MySQL Database
       |
Answer Generator
       |
Natural Language Response
```

### Project Structure

```text
nl-sql-assistant/
├── app.py               # Flask web server and chat endpoint
├── chat_engine.py       # Shared logic for web app and CLI
├── config.py            # Configuration, schema, and constants
├── sql_generator.py     # Natural language to SQL via OpenAI
├── answer_generator.py  # SQL results to natural language via OpenAI
├── db.py                # MySQL connection and query execution
├── utils.py             # SQL validation and logging utilities
├── cli.py               # Command-line interface
├── test_shopbot.py      # Unit tests
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── Procfile             # Render deployment configuration
├── runtime.txt          # Python runtime version
└── templates/
    └── index.html       # Web chat interface
```

## Features

- **Natural Language to SQL** — converts plain English into validated MySQL
  queries using OpenAI GPT-4o-mini
- **Conversation Memory** — retains context across exchanges for follow-up
  questions and pronoun resolution
- **Business Intelligence Mode** — classifies strategic questions and responds
  with GPT-powered business advice
- **SQL Validation** — blocks destructive keywords (DELETE, DROP, INSERT,
  UPDATE) before execution
- **Web Interface** — responsive chat UI with suggested starter questions
- **CLI Interface** — same functionality available from the terminal
- **Modular Design** — single-responsibility modules for readability, testing,
  and maintainability

## Tech Stack

| Layer           | Technology                |
|-----------------|---------------------------|
| Language        | Python 3                  |
| AI              | OpenAI GPT-4o-mini        |
| Database        | MySQL (Aiven)             |
| Web Framework   | Flask                     |
| Deployment      | Render                    |
| DB Connector    | mysql-connector-python    |
| Environment     | python-dotenv             |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/mcklain-still/nl-sql-assistant.git
cd nl-sql-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials (see `.env.example` for the full list).

### 5. Set up the database

Run the following in your MySQL terminal:

```sql
CREATE DATABASE shopbot_db;
USE shopbot_db;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock INT
);

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    quantity INT,
    sale_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### 6. Run the application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

You can also use the CLI version:

```bash
python cli.py
```

## Usage Examples

**Data queries:**

- What products do we sell?
- What is our total revenue?
- Who is our best customer?
- What city are they from?
- Which products are low on stock?

**Business queries:**

- How can we grow our sales?
- Should we expand our product range?
- What marketing strategies should we use?

## Testing

```bash
python -m unittest test_shopbot.py
```

## Deployment

This project is configured for deployment on Render using the included
`Procfile` and `runtime.txt`. Set the following environment variables in your
Render dashboard:

| Variable          | Description                 |
|-------------------|-----------------------------|
| `DB_HOST`         | MySQL host (e.g., Aiven)    |
| `DB_USER`         | MySQL user                  |
| `DB_PASSWORD`     | MySQL password              |
| `DB_NAME`         | MySQL database name         |
| `DB_PORT`         | MySQL port (default: 3306)  |
| `OPENAI_API_KEY`  | OpenAI API key              |

## Skills Demonstrated

- **AI and Prompt Engineering** — production-style OpenAI API integration with
  carefully designed system prompts
- **Database Design** — relational schema with foreign keys, multi-table JOINs,
  and aggregation queries
- **Software Architecture** — modular, single-responsibility design with shared
  logic between web and CLI interfaces
- **Security** — SQL injection prevention through keyword validation and
  SELECT-only enforcement
- **Full Stack Development** — Python Flask backend with HTML, CSS, and
  JavaScript frontend
- **Cloud Deployment** — deployed on Render with managed MySQL on Aiven
- **Problem Solving** — conversation memory, query classification, and graceful
  error handling built from scratch

## License

MIT
