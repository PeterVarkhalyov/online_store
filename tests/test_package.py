"""Тесты публичного интерфейса пакета src."""

import src
from src.category import Category
from src.category_iterator import CategoryIterator
from src.product import Product


def test_package_exports_models() -> None:
    """Основные модели доступны через корневой пакет."""
    assert src.Category is Category
    assert src.CategoryIterator is CategoryIterator
    assert src.Product is Product
    assert src.__all__ == ["Category", "CategoryIterator", "Product"]
