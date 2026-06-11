# NL-SQL Assistant

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46BC99?style=for-the-badge&logo=render&logoColor=white)](https://nl-sql-assistant.onrender.com)

A natural language interface for relational database querying, powered by
OpenAI and MySQL. Converts plain English questions into validated SQL queries
and returns human-readable answers through a web-based chat interface.

## Features

- Natural language to SQL conversion via OpenAI
- Conversation memory for follow-up questions and pronoun resolution
- SQL validation that blocks destructive operations before execution
- Human-readable answer generation from raw query results
- Supports both data queries and business questions grounded in your data
- Web chat interface and CLI support

## Project Structure

```text
nl-sql-assistant/
├── app.py               # Flask web server and chat endpoint
├── chat_engine.py       # Shared logic for web and CLI
├── sql_generator.py     # Natural language to SQL via OpenAI
├── answer_generator.py  # SQL results to natural language via OpenAI
├── db.py                # MySQL connection and query execution
├── config.py            # Configuration, schema, and constants
├── utils.py             # SQL validation and logging utilities
├── cli.py               # Command-line interface
├── test_app.py          # Unit tests
├── schema.sql           # Database and table creation
├── seed.sql             # Sample data
└── templates/
    └── index.html       # Web chat interface
```

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/mcklain-still/nl-sql-assistant.git
cd nl-sql-assistant
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials. See `.env.example` for the full list.

### 3. Set up the database

```bash
mysql -u your_user -p < schema.sql
mysql -u your_user -p shopbot_db < seed.sql
```

### 4. Run the application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser, or use the CLI:

```bash
python cli.py
```

## Usage Examples

- What is our total revenue?
- Who is our best customer?
- Which products are low on stock?
- Who is our top salesperson?
- How are sales trending this quarter?
- Should we expand our product range based on current performance?

## Testing

```bash
python -m unittest test_app.py
```

## Deployment

Configured for Render using the included `Procfile` and `runtime.txt`.
Set the following environment variables in your Render dashboard:

| Variable         | Description                |
| ---------------- | -------------------------- |
| `DB_HOST`        | MySQL host (e.g., Aiven)   |
| `DB_USER`        | MySQL username             |
| `DB_PASSWORD`    | MySQL password             |
| `DB_NAME`        | MySQL database name        |
| `DB_PORT`        | MySQL port (default: 3306) |
| `OPENAI_API_KEY` | OpenAI API key             |

## License

MIT
