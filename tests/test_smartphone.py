"""Тесты модели смартфона."""

import pytest

from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


def test_smartphone_initialization() -> None:
    """Смартфон сохраняет общие и специальные свойства."""
    smartphone = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )

    assert isinstance(smartphone, Product)
    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_smartphone_new_product() -> None:
    """Унаследованный фабричный метод создает смартфон."""
    smartphone = Smartphone.new_product(
        {
            "name": "Iphone 15",
            "description": "512GB, Gray space",
            "price": 210000.0,
            "quantity": 8,
            "efficiency": 90.0,
            "model": "15",
            "memory": 512,
            "color": "Gray space",
        }
    )

    assert isinstance(smartphone, Smartphone)
    assert smartphone.model == "15"
    assert smartphone.memory == 512


def test_same_smartphone_classes_can_be_added() -> None:
    """Два смартфона складываются по стоимости складских остатков."""
    first = Smartphone("A", "Первый", 100.0, 10, 80.0, "A1", 128, "Черный")
    second = Smartphone("B", "Второй", 200.0, 2, 90.0, "B1", 256, "Белый")

    assert first + second == 1400.0


def test_different_product_classes_cannot_be_added() -> None:
    """Смартфон нельзя сложить с газонной травой или обычным товаром."""
    smartphone = Smartphone("A", "Смартфон", 100.0, 10, 80.0, "A1", 128, "Черный")
    grass = LawnGrass("Газон", "Трава", 200.0, 2, "Россия", "7 дней", "Зеленый")
    product = Product("Товар", "Обычный товар", 50.0, 3)

    with pytest.raises(TypeError, match="одинакового класса"):
        smartphone + grass

    with pytest.raises(TypeError, match="одинакового класса"):
        product + smartphone
