"""Модель товара интернет-магазина."""

from typing import Any, Self


class Product:
    """Товар, доступный для продажи."""

    name: str
    description: str
    quantity: int
    __price: float

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализировать товар переданными характеристиками."""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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

    @property
    def price(self) -> float:
        """Вернуть цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Установить новую цену после проверки значения и подтверждения."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input("Подтвердите снижение цены (y/n): ")
            if answer.strip().lower() != "y":
                return

        self.__price = new_price

    def __str__(self) -> str:
        """Вернуть строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Вернуть общую стоимость остатков двух товаров."""
        if type(self) is not type(other):
            raise TypeError("Складывать можно только объекты Product одинакового класса")

        return self.price * self.quantity + other.price * other.quantity
