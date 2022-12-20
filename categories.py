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
        """Заполняет все возможные перечисления слова от категории, которые мы можем записывать, кроме основного"""
        cat_res = []
        for i, cat in enumerate(categories):
            aliases = cat["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(cat["codename"])
            aliases.append(cat["name"])
            cat_res.append(Category(codename=cat["codename"], name=cat["name"], is_base_expense=cat["is_base_expense"], aliases=aliases))
        return cat_res