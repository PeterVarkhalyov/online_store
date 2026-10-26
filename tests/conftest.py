"""Общие фикстуры тестового набора."""

from collections.abc import Generator

import pytest

from src.category import Category


@pytest.fixture(autouse=True)
def reset_category_counters() -> Generator[None, None, None]:
    """Изолировать счетчики категорий и товаров между тестами."""
    Category.category_count = 0
    Category.product_count = 0

    yield

    Category.category_count = 0
    Category.product_count = 0
