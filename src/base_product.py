"""Абстрактная основа всех товаров магазина."""

from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Определить общие свойства и поведение любого товара."""

    name: str
    description: str
    quantity: int
    __price: float

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Сохранить общие характеристики товара."""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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
