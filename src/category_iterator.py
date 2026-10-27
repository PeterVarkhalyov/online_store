"""Итератор товаров одной категории."""

from typing import Self, cast

from src.category import Category
from src.product import Product


class CategoryIterator:
    """Последовательно возвращать товары переданной категории."""

    def __init__(self, category: Category) -> None:
        """Сохранить категорию и установить итератор перед первым товаром."""
        self.category = category
        self.index = 0

    def __iter__(self) -> Self:
        """Сбросить позицию и вернуть текущий итератор."""
        self.index = 0
        return self

    def __next__(self) -> Product:
        """Вернуть очередной товар или завершить итерацию."""
        products = cast(list[Product], getattr(self.category, "_Category__products"))

        if self.index >= len(products):
            raise StopIteration

        product = products[self.index]
        self.index += 1
        return product
