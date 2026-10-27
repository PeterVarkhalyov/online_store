"""Модель заказа одного товара."""

from src.product import Product
from src.product_container import ProductContainer, StockItem


class Order(ProductContainer):
    """Заказ одного товара в заданном количестве."""

    product: Product
    quantity: int
    __unit_price: float

    def __init__(self, product: Product, quantity: int) -> None:
        """Сохранить товар, количество и цену на момент оформления заказа."""
        if not isinstance(product, Product):
            raise TypeError("В заказе должен быть объект класса Product")

        self.product = product
        self.quantity = quantity
        self.__unit_price = product.price

    def _stock_items(self) -> tuple[StockItem, ...]:
        """Вернуть единственную товарную позицию заказа."""
        return ((self.__unit_price, self.quantity),)
