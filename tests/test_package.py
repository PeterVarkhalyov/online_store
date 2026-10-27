"""Тесты публичного интерфейса пакета src."""

import src
from src.category import Category
from src.category_iterator import CategoryIterator
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


def test_package_exports_models() -> None:
    """Основные модели доступны через корневой пакет."""
    assert src.Category is Category
    assert src.CategoryIterator is CategoryIterator
    assert src.LawnGrass is LawnGrass
    assert src.Product is Product
    assert src.Smartphone is Smartphone
    assert src.__all__ == ["Category", "CategoryIterator", "LawnGrass", "Product", "Smartphone"]
