"""Тесты итератора товаров категории."""

import pytest

from src.category import Category
from src.category_iterator import CategoryIterator
from src.product import Product


def test_category_iterator_returns_products_in_order() -> None:
    """Цикл возвращает все товары категории в исходном порядке."""
    products = [
        Product("Товар A", "Описание A", 100.0, 10),
        Product("Товар B", "Описание B", 200.0, 2),
    ]
    iterator = CategoryIterator(Category("Категория", "Описание", products))

    assert list(iterator) == products


def test_category_iterator_protocol() -> None:
    """Итератор возвращает себя и завершает обход через StopIteration."""
    product = Product("Товар", "Описание", 100.0, 1)
    iterator = CategoryIterator(Category("Категория", "Описание", [product]))

    assert iter(iterator) is iterator
    assert next(iterator) is product

    with pytest.raises(StopIteration):
        next(iterator)
