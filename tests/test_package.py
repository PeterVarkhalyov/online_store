"""Тесты публичного интерфейса пакета src."""

import src
from src.base_product import BaseProduct
from src.category import Category
from src.category_iterator import CategoryIterator
from src.exceptions import ZeroQuantityError
from src.lawn_grass import LawnGrass
from src.mixin_log import MixinLog
from src.order import Order
from src.product import Product
from src.product_container import ProductContainer
from src.smartphone import Smartphone


def test_package_exports_models() -> None:
    """Основные модели доступны через корневой пакет."""
    assert src.BaseProduct is BaseProduct
    assert src.Category is Category
    assert src.CategoryIterator is CategoryIterator
    assert src.ZeroQuantityError is ZeroQuantityError
    assert src.LawnGrass is LawnGrass
    assert src.MixinLog is MixinLog
    assert src.Order is Order
    assert src.Product is Product
    assert src.ProductContainer is ProductContainer
    assert src.Smartphone is Smartphone
    assert src.__all__ == [
        "BaseProduct",
        "Category",
        "CategoryIterator",
        "ZeroQuantityError",
        "LawnGrass",
        "MixinLog",
        "Order",
        "Product",
        "ProductContainer",
        "Smartphone",
    ]
