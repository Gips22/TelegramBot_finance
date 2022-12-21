"""Работа с категориями расходов"""
from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    """Структура категории"""
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает все категории расходов из БД"""
        categories = db.fetchall("category", "codename name is_base_expense aliases".split())
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """Заполняет по каждой категории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, категория «кафе» может быть написана как cafe,
        ресторан и тд."""
        cat_res = []
        for i, cat in enumerate(categories):
            aliases = cat["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(cat["codename"])
            aliases.append(cat["name"])
            cat_res.append(Category(
                codename=cat["codename"],
                name=cat["name"],
                is_base_expense=cat["is_base_expense"],
                aliases=aliases
            ))
        return cat_res

    def get_all_categories(self) -> List[Dict]:
        """Возвращает справочник категорий"""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        found = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found
