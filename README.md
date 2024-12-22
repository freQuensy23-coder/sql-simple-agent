# SQL Analysis Assistant

An interactive AI-powered SQL analysis tool that combines OpenAI's GPT-4 with a sandboxed environment for running SQL queries and Python code.

## Features

- Natural language interface for SQL queries
- Secure code execution in a Docker sandbox
- Support for SQL-to-Parquet file conversion
- Interactive data exploration
- Built-in mock database with sample data

## Prerequisites

- Python 3.12+
- Docker
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install openai pandas llm-sandbox faker sqlite3
```

4. Set up your environment variables:
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Initialize the mock database (only needed once):
```bash
python mock_database.py
```

2. Start the assistant:
```bash
python main.py
```

3. Interact with the assistant using natural language. Example queries:
- "Show me the top 5 most expensive products"
- "Calculate total sales for each employee"
- "Save all orders from last month to a parquet file"

## Project Structure

- `main.py` - Main application entry point
- `functional.py` - Core SQL and data processing functions
- `tools.py` - Tool definitions for the AI assistant
- `mock_database.py` - Database initialization and sample data generation
- `prompts.py` - System prompts and schema descriptions

## Features

- **SQL Query Execution**: Run SQL queries against the SQLite database
- **Data Preview**: View sample data (first 4 rows) from query results
- **Parquet Export**: Save query results to Parquet files
- **Python Code Execution**: Run Python code in a sandboxed environment
- **Interactive Assistant**: Natural language interface powered by GPT-4

## Security

All code execution happens in a Docker sandbox environment, ensuring system safety and isolation.

## License

[Your chosen license]
