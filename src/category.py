"""Модель категории товаров интернет-магазина."""

from src.product import Product


class Category:
    """Категория и относящиеся к ней товары."""

    name: str
    description: str
    __products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product] | None = None) -> None:
        """Инициализировать категорию и обновить общие счетчики."""
        self.name = name
        self.description = description
        self.__products = []

        Category.category_count += 1

        for product in products or []:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        """Добавить товар в категорию."""
        if not isinstance(product, Product):
            raise TypeError("Добавлять можно только объекты класса Product")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Вернуть строковое представление всех товаров категории."""
        return "".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n" for product in self.__products
        )
