# Shop Bot 🏪

A natural-language-to-SQL AI assistant for store database queries. Converts English questions into SQL queries and returns natural-language answers.

## Architecture

This project demonstrates:
- **NLP + SQL**: Converting natural language to structured queries
- **Prompt Engineering**: Crafted prompts to guide LLM behavior
- **Safety & Validation**: SQL validation to prevent unsafe queries
- **Modular Design**: Separated concerns for testing and maintainability

### Key Components

- **`config.py`**: Configuration and schema definition
- **`sql_generator.py`**: Converts questions → SQL via OpenAI
- **`db.py`**: Database connection and query execution
- **`answer_generator.py`**: Converts results → natural language
- **`cli.py`**: User-facing CLI interface
- **`utils.py`**: Validation and utility functions

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

3. **Run the bot**:
   ```bash
   python cli.py
   ```

## Features

✅ Natural language question processing  
✅ SQL generation via GPT-3.5-turbo  
✅ SQL validation (prevents DELETE, DROP, etc.)  
✅ Error handling and logging  
✅ Formatted result presentation  

## Safety

- Only `SELECT` statements allowed
- Forbidden keywords: `DELETE`, `DROP`, `INSERT`, `UPDATE`, etc.
- Comment injection prevention
- Comprehensive error handling

## Testing

Run tests with:
```bash
python -m unittest test_shopbot.py
```

## Example Queries

- "What products are in stock?"
- "How many customers are from New York?"
- "What's the total revenue from sales?"
- "List products under $50"

## Project Structure

```
SQL-Chat/
├── config.py               # Configuration and constants
├── db.py                   # Database operations
├── sql_generator.py        # SQL generation with LLM
├── answer_generator.py     # Natural language answer generation
├── utils.py                # Validation and utilities
├── cli.py                  # Main CLI interface
├── test_shopbot.py         # Unit tests
├── requirements.txt        # Dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## License

MIT
