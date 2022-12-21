"""Запросы в БД вынесены в этот модуль"""
import os
from typing import Dict, Tuple, List

import sqlite3

connection = sqlite3.connect(os.path.join("db", "telegram_finance.db"))
cursor = connection.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join('?' * len(column_values.keys()))
    cursor.executemany(
        f"insert into {table}"
        f"({columns})"  # узнать тут про f строку
        f"values ({placeholders})",
        values)
    connection.commit()

def fetchall(table:str, columns: List[str]) -> List[Tuple]:
    columns_joined = ', '.join(columns)
    cursor.execute(f"select {columns_joined} from {table}")
    rows = cursor.fetchall()
    rez = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        rez.append(dict_row)
    return rez
