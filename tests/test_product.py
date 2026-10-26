"""Тесты модели товара."""

from src.product import Product


def test_product_initialization() -> None:
    """Все переданные характеристики сохраняются в объекте товара."""
    product = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5
