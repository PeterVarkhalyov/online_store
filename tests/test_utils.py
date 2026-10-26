"""Тесты преобразования JSON-данных в модели магазина."""

import json
from pathlib import Path

from src.category import Category
from src.product import Product
from src.utils import load_categories_from_json


def test_load_categories_from_json_creates_models(tmp_path: Path) -> None:
    """Категории и вложенные товары создаются с корректными значениями."""
    data = [
        {
            "name": "Смартфоны",
            "description": "Смартфоны и аксессуары",
            "products": [
                {
                    "name": "Iphone 15",
                    "description": "512GB, Gray space",
                    "price": 210000.0,
                    "quantity": 8,
                }
            ],
        }
    ]
    file_path = tmp_path / "products.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(file_path)

    assert len(categories) == 1
    assert isinstance(categories[0], Category)
    assert categories[0].name == "Смартфоны"
    assert categories[0].description == "Смартфоны и аксессуары"
    assert len(categories[0].products) == 1
    assert isinstance(categories[0].products[0], Product)
    assert categories[0].products[0].name == "Iphone 15"
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_load_categories_from_json_skips_invalid_categories(tmp_path: Path) -> None:
    """Поврежденные категории пропускаются, а корректные загружаются."""
    data = [
        "не объект",
        {"name": "Ошибка", "description": "Ошибка", "products": "не список"},
        {"name": 123, "description": "Название не является строкой", "products": []},
        {"name": "Пустая категория", "description": "Без товаров", "products": []},
    ]
    file_path = tmp_path / "products.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(file_path)

    assert len(categories) == 1
    assert categories[0].name == "Пустая категория"
    assert categories[0].products == []


def test_load_categories_from_json_returns_empty_list_for_object_root(tmp_path: Path) -> None:
    """JSON с объектом вместо списка категорий не загружается."""
    file_path = tmp_path / "products.json"
    file_path.write_text('{"name": "Смартфоны"}', encoding="utf-8")

    assert load_categories_from_json(file_path) == []
