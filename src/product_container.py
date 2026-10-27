"""Абстрактная основа объектов, содержащих товары."""

from abc import ABC, abstractmethod

StockItem = tuple[float, int]


class ProductContainer(ABC):
    """Предоставить общие свойства количества и стоимости товаров."""

    @abstractmethod
    def _stock_items(self) -> tuple[StockItem, ...]:
        """Вернуть пары цены и количества товарных позиций."""
        ...

    @property
    def total_quantity(self) -> int:
        """Вернуть суммарное количество товаров."""
        return sum(quantity for _, quantity in self._stock_items())

    @property
    def total_cost(self) -> float:
        """Вернуть суммарную стоимость товаров."""
        return sum(price * quantity for price, quantity in self._stock_items())
