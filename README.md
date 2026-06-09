# Store Analytics Assistant

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46BC99?style=for-the-badge&logo=render&logoColor=white)](https://nl-sql-assistant.onrender.com)

A natural language interface for relational database querying, powered by OpenAI and MySQL. Converts plain English questions into validated SQL queries and returns human-readable answers through a web-based chat interface.

## Project Structure

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
├── schema.sql           # Database and table creation
├── seed.sql             # Sample data for demo usage
├── .env.example         # Environment variable template
├── Procfile             # Render deployment configuration
├── runtime.txt          # Python runtime version
└── templates/
    └── index.html       # Web chat interface
```

## Features

- **Conversation Memory** — retains context across exchanges for follow-up questions and pronoun resolution
- **SQL Validation** — blocks destructive keywords (DELETE, DROP, INSERT, UPDATE) before execution
- **Web Interface** — responsive chat UI with suggested starter questions

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

Create the database and tables:

```bash
mysql -u your_user -p < schema.sql
```

Then populate it with sample data:

```bash
mysql -u your_user -p shopbot_db < seed.sql
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
- Which products are low on stock?
- What is the average rating for each product?
- Which supplier has the most products?
- Who is our top salesperson?
- Which employee made the most sales?
- What is the average salary by position?

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

## License

MIT
