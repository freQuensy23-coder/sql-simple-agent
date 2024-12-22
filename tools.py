from openai.types.chat import ChatCompletionToolParam

tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "run_sql_and_view_table_subset",
            "description": "Run sql query and return first 4 rows of result with cleaned data (remove extra symbols, etc.) to better LLM performance. Use this to check schema of the table.",
            "parameters": {
                "type": "object",
                "properties": {"sql_query": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_sql_and_save_to_parquet",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"},
                    "file_name": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Run python code and return result. User print() to output result. Also you can save some results to file if it is needed",
            "parameters": {
                "type": "object",
                "properties": {"python_code": {"type": "string"}},
            },
        },
    },
]
