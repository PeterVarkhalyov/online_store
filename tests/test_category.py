"""Тесты модели категории."""

import pytest

from src.category import Category
from src.exceptions import ZeroQuantityError
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


def test_category_initialization() -> None:
    """Все переданные характеристики сохраняются в объекте категории."""
    products = [
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]
    category = Category(
        "Смартфоны",
        "Смартфоны и аксессуары",
        products,
    )

    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны и аксессуары"
    assert category.products == (
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n" "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
    )


def test_products_are_private() -> None:
    """К приватному списку товаров нельзя обратиться по исходному имени."""
    category = Category("Смартфоны", "Смартфоны и аксессуары")

    with pytest.raises(AttributeError):
        getattr(category, "__products")


def test_add_product() -> None:
    """Метод добавляет товар и обновляет общий счетчик."""
    category = Category("Смартфоны", "Смартфоны и аксессуары")
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    category.add_product(product)

    assert category.products == "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    assert Category.product_count == 1


def test_add_product_reports_success_and_completion(capsys: pytest.CaptureFixture[str]) -> None:
    """Успешное добавление сообщает о результате и завершении обработки."""
    category = Category("Смартфоны", "Смартфоны и аксессуары")
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    capsys.readouterr()

    category.add_product(product)

    assert capsys.readouterr().out == "Товар успешно добавлен.\nОбработка добавления товара завершена.\n"


def test_add_product_rejects_zero_quantity(capsys: pytest.CaptureFixture[str]) -> None:
    """Нулевой остаток не добавляется, а обработка всегда завершается."""
    category = Category("Смартфоны", "Смартфоны и аксессуары")
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product.quantity = 0
    capsys.readouterr()

    with pytest.raises(ZeroQuantityError):
        category.add_product(product)

    assert category.products == ""
    assert Category.product_count == 0
    assert capsys.readouterr().out == (
        "Товар с нулевым количеством не может быть добавлен.\n" "Обработка добавления товара завершена.\n"
    )


def test_add_product_rejects_other_types() -> None:
    """В категорию разрешено добавлять только объекты Product."""
    category = Category("Смартфоны", "Смартфоны и аксессуары")

    with pytest.raises(TypeError, match="Product"):
        category.add_product("не товар")


def test_add_product_accepts_product_and_its_subclasses() -> None:
    """Категория принимает обычные товары, смартфоны и газонную траву."""
    category = Category("Смешанная категория", "Разные товары")
    product = Product("Товар", "Обычный товар", 50.0, 3)
    smartphone = Smartphone("Смартфон", "Телефон", 100.0, 2, 80.0, "A1", 128, "Черный")
    grass = LawnGrass("Газон", "Трава", 200.0, 1, "Россия", "7 дней", "Зеленый")

    category.add_product(product)
    category.add_product(smartphone)
    category.add_product(grass)

    assert Category.product_count == 3
    assert "Товар, 50.0 руб. Остаток: 3 шт." in category.products
    assert "Смартфон, 100.0 руб. Остаток: 2 шт." in category.products
    assert "Газон, 200.0 руб. Остаток: 1 шт." in category.products


def test_product_count() -> None:
    """Счетчик товаров учитывает товары во всех созданных категориях."""
    smartphones = [
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]
    televisions = [Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)]

    Category("Смартфоны", "Смартфоны и аксессуары", smartphones)
    Category("Телевизоры", "Телевизоры и аксессуары", televisions)

    assert Category.product_count == 3


def test_category_count() -> None:
    """Счетчик категорий увеличивается для каждого созданного объекта."""
    Category("Смартфоны", "Смартфоны и аксессуары")
    Category("Телевизоры", "Телевизоры и аксессуары")

    assert Category.category_count == 2


def test_empty_category_products() -> None:
    """Геттер пустой категории возвращает пустую строку."""
    category = Category("Пустая категория", "Без товаров")

    assert category.products == ""


def test_middle_price() -> None:
    """Средняя цена рассчитывается по всем товарам категории."""
    category = Category(
        "Тестовая категория",
        "Описание",
        [
            Product("Товар A", "Описание A", 100.0, 10),
            Product("Товар B", "Описание B", 200.0, 2),
        ],
    )

    assert category.middle_price() == 150.0


def test_middle_price_of_empty_category() -> None:
    """Средняя цена пустой категории равна нулю."""
    category = Category("Пустая категория", "Без товаров")

    assert category.middle_price() == 0


def test_category_string_representation() -> None:
    """Категория выводит суммарное количество всех товаров на складе."""
    products = [
        Product("Товар A", "Описание A", 100.0, 10),
        Product("Товар B", "Описание B", 200.0, 2),
    ]
    category = Category("Тестовая категория", "Описание", products)

    assert str(category) == "Тестовая категория, количество продуктов: 12 шт."
