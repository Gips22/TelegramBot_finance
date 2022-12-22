"""Работа с расходами - их добавление, удаление, статистика."""
import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions
from categories import Categories

class Message(NamedTuple):
    """Структура распаршенного сообщения о расходе"""
    amount: int
    category_text: str

class Expense(NamedTuple):
    """Структура добавленного в БД новго расхода"""
    id: Optional[int]
    amount: int
    category_name: str

# TODO: разобрать регулярку
def _parse_message(raw_message: str) -> Message:
    """Парсит пришедшее в бот сообщение"""
    # regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    # if not regexp_result or not regexp_result.group(0) \
    #         or not regexp_result.group(1) or not regexp_result.group(2):
    #     raise exceptions.NotCorrectMessage(
    #         "Не могу понять сообщение. Напишите сообщение в формате, "
    #         "например:\n1500 метро")
    message_part1, message_part2 = raw_message.split()
    if str(message_part1).isdigit() and str(message_part2).isalpha():
        amount = message_part1
        category_text = message_part2
    elif str(message_part2).isdigit() and str(message_part1).isalpha():
        amount = message_part2
        category_text = message_part1
    else:
        raise exceptions.NotCorrectMessage("Некорректное сообщение. Попробуйте ввести в другом формате")
    return Message(amount=amount, category_text=category_text)


def add_expense(raw_message: str) -> Expense:
    """Добавляет и сохраняет в БД новый расход. Принимает на вход сообщение из бота."""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category()
