"""Модель категории товаров интернет-магазина."""

from src.product import Product


class Category:
    """Категория и относящиеся к ней товары."""

    name: str
    description: str
    products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product] | None = None):
        """Инициализировать категорию и обновить общие счетчики."""
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(products) if products is not None else 0
