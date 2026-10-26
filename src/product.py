"""Модель товара интернет-магазина."""


class Product:
    """Товар, доступный для продажи."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализировать товар переданными характеристиками."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
