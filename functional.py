import pandas as pd
from llm_sandbox.docker import SandboxDockerSession
import os


def sql2pandas(sql_query: str, db) -> pd.DataFrame:
    cursor = db.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[i[0] for i in cursor.description])


def sql2parquet(sql_query: str, file_name: str, db, docker_session: SandboxDockerSession) -> None:
    df = sql2pandas(sql_query, db)
    df.to_parquet(file_name)
    docker_session.copy_to_runtime(src=os.path.abspath(file_name), dest='/')


def sql2str(sql_query: str, db) -> str:
    """Возвращает строку с первыми 4 строками таблицы. Так же отчищает от лишних символов итп, что бы тратить меньше токенов"""
    df = sql2pandas(sql_query, db)
    df = df.iloc[:4]
    for column in df.columns:
        df[column] = df[column].astype(str)
        df[column] = df[column].apply(lambda x: x[:200] + "..." if len(x) > 200 else x)
    return df.to_string() + f'\n..... and {len(df) -4} rows. Use save to parquet to save the rest of the data.'
