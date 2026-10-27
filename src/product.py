"""Модель товара интернет-магазина."""

from typing import Any, Self

from src.base_product import BaseProduct
from src.mixin_log import MixinLog


class Product(MixinLog, BaseProduct):
    """Товар, доступный для продажи."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализировать товар переданными характеристиками."""
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(
        cls,
        product_data: dict[str, Any],
        products: list[Self] | None = None,
    ) -> Self:
        """Создать товар или объединить его с одноименным товаром."""
        for product in products or []:
            if product.name == product_data["name"]:
                product.quantity += product_data["quantity"]
                if product_data["price"] > product.price:
                    product.price = product_data["price"]
                return product

        return cls(**product_data)

    def __add__(self, other: "Product") -> float:
        """Вернуть общую стоимость остатков двух товаров."""
        if type(self) is not type(other):
            raise TypeError("Складывать можно только объекты Product одинакового класса")

        return self.price * self.quantity + other.price * other.quantity
