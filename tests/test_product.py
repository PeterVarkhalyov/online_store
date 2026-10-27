"""Тесты модели товара."""

import pytest

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


def test_product_rejects_zero_quantity() -> None:
    """Товар с нулевым количеством нельзя создать."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Товар", "Описание", 100.0, 0)


def test_price_is_private() -> None:
    """К приватному атрибуту цены нельзя обратиться по исходному имени."""
    product = Product("Товар", "Описание", 100.0, 1)

    with pytest.raises(AttributeError):
        getattr(product, "__price")


def test_new_product_creates_product_from_dictionary() -> None:
    """Фабричный метод создает товар из словаря."""
    product = Product.new_product(
        {
            "name": "Iphone 15",
            "description": "512GB, Gray space",
            "price": 210000.0,
            "quantity": 8,
        }
    )

    assert isinstance(product, Product)
    assert product.name == "Iphone 15"
    assert product.description == "512GB, Gray space"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_new_product_merges_duplicate_and_selects_higher_price() -> None:
    """Дубликат увеличивает остаток и сохраняет наиболее высокую цену."""
    existing_product = Product("Iphone 15", "512GB", 200000.0, 3)

    product = Product.new_product(
        {
            "name": "Iphone 15",
            "description": "512GB, Gray space",
            "price": 210000.0,
            "quantity": 5,
        },
        [existing_product],
    )

    assert product is existing_product
    assert product.quantity == 8
    assert product.price == 210000.0


def test_new_product_does_not_reduce_duplicate_price() -> None:
    """Более низкая цена дубликата не заменяет текущую цену."""
    existing_product = Product("Iphone 15", "512GB", 210000.0, 3)

    product = Product.new_product(
        {
            "name": "Iphone 15",
            "description": "512GB, Gray space",
            "price": 190000.0,
            "quantity": 5,
        },
        [existing_product],
    )

    assert product is existing_product
    assert product.quantity == 8
    assert product.price == 210000.0


@pytest.mark.parametrize("new_price", [0, -100.0])
def test_price_rejects_non_positive_value(new_price: float, capsys: pytest.CaptureFixture[str]) -> None:
    """Нулевая и отрицательная цена отклоняются с сообщением."""
    product = Product("Товар", "Описание", 100.0, 1)
    capsys.readouterr()

    product.price = new_price

    assert product.price == 100.0
    assert capsys.readouterr().out == "Цена не должна быть нулевая или отрицательная\n"


def test_price_increase_does_not_require_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Повышение цены выполняется без запроса пользователю."""
    product = Product("Товар", "Описание", 100.0, 1)

    def fail_on_input(prompt: str) -> str:
        raise AssertionError("input не должен вызываться при повышении цены")

    monkeypatch.setattr("builtins.input", fail_on_input)
    product.price = 120.0

    assert product.price == 120.0


def test_price_decrease_is_applied_after_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ответ y подтверждает снижение цены."""
    product = Product("Товар", "Описание", 100.0, 1)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    product.price = 80.0

    assert product.price == 80.0


def test_price_decrease_is_cancelled_without_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Любой ответ, кроме y, отменяет снижение цены."""
    product = Product("Товар", "Описание", 100.0, 1)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = 80.0

    assert product.price == 100.0


def test_product_string_representation() -> None:
    """Товар преобразуется в строку установленного формата."""
    product = Product("Товар", "Описание", 80.0, 15)

    assert str(product) == "Товар, 80.0 руб. Остаток: 15 шт."


def test_products_addition_returns_total_stock_value() -> None:
    """Сложение товаров возвращает полную стоимость обоих остатков."""
    product_a = Product("Товар A", "Описание A", 100.0, 10)
    product_b = Product("Товар B", "Описание B", 200.0, 2)

    assert product_a + product_b == 1400.0


def test_product_addition_rejects_other_types() -> None:
    """Товар нельзя складывать с объектом другого типа."""
    product = Product("Товар", "Описание", 100.0, 10)

    with pytest.raises(TypeError, match="Product"):
        product + 1  # type: ignore[operator]
