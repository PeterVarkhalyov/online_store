"""Тесты абстрактного товара и миксина журналирования."""

import pytest

from src.base_product import BaseProduct
from src.mixin_log import MixinLog
from src.product import Product


def test_base_product_is_abstract_parent() -> None:
    """Абстрактный товар нельзя создать напрямую, а Product наследует его."""
    assert issubclass(Product, BaseProduct)

    with pytest.raises(TypeError):
        BaseProduct("Товар", "Описание", 100.0, 1)  # type: ignore[abstract]


def test_mixin_log_prints_created_product(capsys: pytest.CaptureFixture[str]) -> None:
    """Миксин печатает класс и параметры созданного объекта."""
    product = Product("Продукт1", "Описание продукта", 1200, 10)

    assert capsys.readouterr().out == "Product('Продукт1', 'Описание продукта', 1200, 10)\n"
    assert repr(product) == "Product('Продукт1', 'Описание продукта', 1200, 10)"
    assert Product.__mro__.index(MixinLog) < Product.__mro__.index(BaseProduct)
