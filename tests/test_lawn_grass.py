"""Тесты модели газонной травы."""

from src.lawn_grass import LawnGrass
from src.product import Product


def test_lawn_grass_initialization() -> None:
    """Газонная трава сохраняет общие и специальные свойства."""
    grass = LawnGrass(
        "Газонная трава",
        "Смесь семян для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )

    assert isinstance(grass, Product)
    assert grass.name == "Газонная трава"
    assert grass.description == "Смесь семян для газона"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_same_lawn_grass_classes_can_be_added() -> None:
    """Два товара газонной травы складываются по стоимости остатков."""
    first = LawnGrass("Газон A", "Трава A", 100.0, 10, "Россия", "7 дней", "Зеленый")
    second = LawnGrass("Газон B", "Трава B", 200.0, 2, "Германия", "10 дней", "Темно-зеленый")

    assert first + second == 1400.0
