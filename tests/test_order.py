"""Тесты заказа и общего абстрактного контейнера."""

import pytest

from src.category import Category
from src.order import Order
from src.product import Product
from src.product_container import ProductContainer


def test_product_container_is_abstract_parent() -> None:
    """Контейнер нельзя создать напрямую, а Category и Order наследуют его."""
    assert issubclass(Category, ProductContainer)
    assert issubclass(Order, ProductContainer)

    with pytest.raises(TypeError):
        ProductContainer()  # type: ignore[abstract]


def test_order_initialization() -> None:
    """Заказ хранит один товар, количество и итоговую стоимость."""
    product = Product("Кофе", "Зерновой кофе", 500.0, 10)
    order = Order(product, 3)

    assert order.product is product
    assert order.quantity == 3
    assert order.total_quantity == 3
    assert order.total_cost == 1500.0


def test_order_keeps_cost_at_creation_time() -> None:
    """Стоимость заказа не меняется после повышения цены товара."""
    product = Product("Кофе", "Зерновой кофе", 500.0, 10)
    order = Order(product, 2)

    product.price = 600.0

    assert order.total_cost == 1000.0


def test_order_rejects_non_product() -> None:
    """В заказ нельзя передать объект, не являющийся товаром."""
    with pytest.raises(TypeError, match="Product"):
        Order("не товар", 1)  # type: ignore[arg-type]


def test_category_uses_common_container_properties() -> None:
    """Категория рассчитывает общее количество и стоимость через базовый класс."""
    category = Category(
        "Напитки",
        "Кофе и чай",
        [
            Product("Кофе", "Зерновой", 500.0, 2),
            Product("Чай", "Черный", 200.0, 3),
        ],
    )

    assert category.total_quantity == 5
    assert category.total_cost == 1600.0
