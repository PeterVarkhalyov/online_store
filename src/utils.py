"""Создание объектов предметной области из файлов с данными."""

import logging
from collections.abc import Mapping
from pathlib import Path

from src.category import Category
from src.fields import _load_field_aliases, get_field_value
from src.product import Product
from src.readers import get_fields_from_json

PRODUCTS_FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "products.json"

FIELD_ALIASES = _load_field_aliases()

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
logger.propagate = False

file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_categories_from_json(file_path: str | Path = PRODUCTS_FILE_PATH) -> list[Category]:
    """Загрузить категории и их товары из JSON-файла."""
    logger.debug("Начало загрузки категорий из файла: %s", file_path)
    data = get_fields_from_json(file_path)

    if not isinstance(data, list):
        logger.error(
            "Не удалось загрузить категории из %s: ожидался список, получено %s",
            file_path,
            type(data).__name__,
        )
        return []

    categories: list[Category] = []

    for category_number, category_data in enumerate(data, start=1):
        try:
            if not isinstance(category_data, Mapping):
                raise TypeError("данные категории должны быть объектом")

            products_data = get_field_value(category_data, "products", FIELD_ALIASES)
            if not isinstance(products_data, list):
                raise TypeError("товары категории должны быть списком")

            products = [Product(**product_data) for product_data in products_data]
            name = get_field_value(category_data, "name", FIELD_ALIASES)
            description = get_field_value(category_data, "description", FIELD_ALIASES)

            if not isinstance(name, str) or not isinstance(description, str):
                raise TypeError("название и описание категории должны быть строками")

            categories.append(
                Category(
                    name=name,
                    description=description,
                    products=products,
                )
            )

        except (KeyError, TypeError, ValueError) as error:
            logger.error(
                "Не удалось обработать категорию №%d из файла %s: %s",
                category_number,
                file_path,
                error,
            )

    logger.info(
        "Успешно загружено категорий из файла %s: %d",
        file_path,
        len(categories),
    )

    return categories
