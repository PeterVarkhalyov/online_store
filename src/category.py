"""Модель категории товаров интернет-магазина."""

from src.exceptions import ZeroQuantityError
from src.product import Product
from src.product_container import ProductContainer, StockItem


class Category(ProductContainer):
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

    def add_product(self, product: object) -> None:
        """Проверить объект и добавить товар или его наследника в категорию."""
        if not isinstance(product, Product) or not issubclass(type(product), Product):
            raise TypeError("Добавлять можно только объекты класса Product")

        try:
            if product.quantity == 0:
                raise ZeroQuantityError
        except ZeroQuantityError as error:
            print(error)
            raise
        else:
            self.__products.append(product)
            Category.product_count += 1
            print("Товар успешно добавлен.")
        finally:
            print("Обработка добавления товара завершена.")

    @property
    def products(self) -> str:
        """Вернуть строковое представление всех товаров категории."""
        return "".join(f"{product}\n" for product in self.__products)

    def __str__(self) -> str:
        """Вернуть название категории и общий остаток всех ее товаров."""
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."

    def middle_price(self) -> float:
        """Вернуть среднюю цену товаров категории или ноль для пустой категории."""
        try:
            return sum(product.price for product in self.__products) / len(self.__products)
        except ZeroDivisionError:
            return 0

    def _stock_items(self) -> tuple[StockItem, ...]:
        """Вернуть цены и остатки всех товаров категории."""
        return tuple((product.price, product.quantity) for product in self.__products)
