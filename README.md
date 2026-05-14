# Store Analytics Assistant

A natural language interface for relational database querying, powered by OpenAI and MySQL. Converts plain English questions into validated SQL queries and returns human-readable answers through a web-based chat interface.

## Overview

This project demonstrates an end-to-end AI-driven query layer that bridges conversational AI and structured data. It was built to showcase practical skills in prompt engineering, database design, API integration, and full stack Python development.

## Demo

| Question | Type | Response |
|---|---|---|
| "What is our best selling product?" | Data | Queries sales table, returns ranked results |
| "Who is our best customer?" | Data | JOINs customers, sales, and products tables |
| "What city are they from?" | Follow-up | Resolves context from previous answer |
| "How can we grow our electronics sales?" | Business | GPT-powered strategic recommendation |

## Architecture
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

### Project Structure
store-analytics-assistant/
├── app.py                  # Flask web server and chat endpoint
├── config.py               # Configuration, schema, and constants
├── sql_generator.py        # Natural language to SQL via OpenAI
├── answer_generator.py     # SQL results to natural language via OpenAI
├── db.py                   # MySQL connection and query execution
├── utils.py                # SQL validation and logging utilities
├── cli.py                  # Command-line interface
├── test_shopbot.py         # Unit tests
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── templates/
└── index.html          # Web chat interface

## Features

- **Natural Language to SQL** — converts plain English into validated MySQL queries using GPT-3.5-turbo
- **Conversation Memory** — retains context across exchanges for follow-up questions and pronoun resolution
- **Business Intelligence Mode** — classifies strategic questions and responds with GPT-powered business advice
- **SQL Validation** — blocks destructive keywords (DELETE, DROP, INSERT, UPDATE) before execution
- **Automatic Retry Logic** — retries failed queries silently before surfacing errors to the user
- **Web Interface** — responsive chat UI with suggested starter questions
- **Modular Design** — single-responsibility modules for readability, testing, and maintainability

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| AI | OpenAI GPT-3.5-turbo |
| Database | MySQL |
| Web Framework | Flask |
| DB Connector | mysql-connector-python |
| Environment | python-dotenv |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/mcklain-still/store-analytics-assistant.git
cd store-analytics-assistant
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

Edit `.env` with your credentials:
OPENAI_API_KEY=your_openai_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=shopbot_db

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

## Usage Examples

**Data queries:**
- "What products do we sell?"
- "What is our total revenue?"
- "Who is our best customer?"
- "What city are they from?"
- "What does she buy?"
- "Which products are low on stock?"

**Business queries:**
- "How can we grow our sales?"
- "Should we expand our product range?"
- "What marketing strategies should we use?"

## Testing

```bash
python -m unittest test_shopbot.py
```

## Future Improvements

- User authentication and multi-session support
- CSV export for query results
- Dynamic schema introspection
- Fine-tuned model for improved SQL accuracy
- Cloud deployment (AWS or Heroku)
- Data visualization dashboard

## Skills Demonstrated

- **AI and Prompt Engineering** — production-style OpenAI API integration with carefully designed system prompts and retry logic
- **Database Design** — relational schema with foreign keys, multi-table JOINs, and aggregation queries
- **Software Architecture** — modular, single-responsibility design across seven independent files
- **Security** — SQL injection prevention through keyword validation and SELECT-only enforcement
- **Full Stack Development** — Python Flask backend with HTML, CSS, and JavaScript frontend
- **Problem Solving** — conversation memory, query classification, and graceful error handling built from scratch

## License

MIT