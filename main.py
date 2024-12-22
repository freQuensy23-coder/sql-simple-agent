from typing import Callable
from openai import Client
from pprint import pprint
import pandas as pd
import json
from tools import tools
import os
from llm_sandbox import SandboxSession
from prompts import schema_description
from functional import sql2str, sql2parquet
import sqlite3
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionToolMessageParam,
)

def run_function_safe(function: Callable, args: list = [], kwargs: dict = {}) -> str:
    """
    Запускает переданную функцию, перехватывая любые исключения.
    Возвращает результат выполнения функции либо текст ошибки.
    """
    try:
        return function(*args, **kwargs)
    except Exception as e:
        print('Durring execution of function', function.__name__, 'occurred error:', e)
        return f"Error: {e}"

# Инициализация клиента и базы данных
client = Client()
db = sqlite3.connect("database.sqlite")
print("Database connected")

SYSTEM_MESSAGE = ChatCompletionSystemMessageParam(
    role="system",
    content=(
        "You are a helpful assistant that can run SQL commands.\n"
        "Database schema:\n"
        + schema_description
    ),
)

# Изначальная история сообщений содержит только системное сообщение
history: list = [SYSTEM_MESSAGE]

# Флаг, показывающий, нужно ли снова запрашивать у пользователя ввод
need_user_intent: bool = True

print('Creating docker sandbox to run llm code. It can take some time, especially on first run.')
with SandboxSession(lang="python", dockerfile=os.path.abspath('Dockerfile')) as session:
    print('Docker sandbox created')
    while True:
        # Если нужен новый ввод от пользователя — запрашиваем
        if need_user_intent:
            user_input: str = input("You: ")
            print("---------- \n \n")
            if user_input == "exit":
                break
            # Добавляем сообщение пользователя в историю
            history.append(ChatCompletionUserMessageParam(role="user", content=user_input))

        # Делаем запрос к чат-модели
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=history,
            tools=tools,
        )

        # Ответ модели
        llm_answer: str = str(completion.choices[0].message.content)
        

        # Проверяем, есть ли у ассистента вызовы функций
        if completion.choices[0].message.tool_calls:
            # Сами добавляем это сообщение-«заголовок» ассистента (с вызовами функций) в историю
            history.append(completion.choices[0].message)

            # ВАЖНО: обрабатываем **все** tool_calls, а не только первый
            for tool_call in completion.choices[0].message.tool_calls:
                tool_name: str = tool_call.function.name
                tool_args = tool_call.function.arguments

                # В зависимости от имени инструмента выполняем разные действия
                match tool_name:
                    case "run_sql_and_view_table_subset":
                        print(f'   >  смотрю на данные по запросу {tool_args.replace("\\n", " ").replace("\\t", " ").replace("\n", " ")}')
                        data = json.loads(tool_args)
                        sql_query: str = data["sql_query"]
                        result: str = run_function_safe(sql2str, [sql_query, db])
                        # Отправляем отдельное сообщение с ролью "tool"
                        history.append(
                            ChatCompletionToolMessageParam(
                                role="tool",
                                content=result,
                                tool_call_id=tool_call.id,
                            )
                        )

                    case "run_sql_and_save_to_parquet":
                        data = json.loads(tool_args)
                        sql_query: str = data["sql_query"]
                        file_name: str = data["file_name"]
                        print(f'   >  сохраняю данные по запросу {tool_args.replace("\\n", " ").replace("\\t", " ").replace("\n", " ")} в файл {file_name}')
                        result: str = run_function_safe(sql2parquet, [sql_query, file_name, db, session])
                        # Отправляем отдельное сообщение с ролью "tool"
                        history.append(
                            ChatCompletionToolMessageParam(
                                role="tool",
                                content=f"File {file_name} saved",
                                tool_call_id=tool_call.id,
                            )
                        )

                    case "run_python":
                        
                        data = json.loads(tool_args)
                        python_code: str = data["python_code"]
                        print(f'   >  выполняю python код ```{python_code.replace('\n', '')}```')
                        python_code = python_code.replace('\\n', '\n').replace('\\t', '\t')

                        result = session.run(python_code).text

                        print(f'   >  результат выполнения python кода: {result}')
                        # Отправляем отдельное сообщение с ролью "tool"
                        history.append(
                            ChatCompletionToolMessageParam(
                                role="tool",
                                content=f"Python code executed with result: {result}",
                                tool_call_id=tool_call.id,
                            )
                        )

            # После обработки всех инструментов на это сообщение — модель может ещё продолжить говорить
            # (но, по условию, в оригинальном коде мы ожидаем, что не нужно заново ввод от пользователя)
            need_user_intent = False

        else:
            # Нет вызовов функций в сообщении ассистента — просто выводим текст
            need_user_intent = True
            print("LLM says:", completion.choices[0].message.content)