"""Миксин журналирования создания объектов."""

from inspect import signature
from typing import Any


class MixinLog:
    """Печатать представление объекта после его инициализации."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Передать параметры по MRO и вывести созданный объект."""
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self) -> str:
        """Вернуть имя фактического класса и параметры его конструктора."""
        parameter_names = (name for name in signature(type(self).__init__).parameters if name != "self")
        parameters = ", ".join(repr(getattr(self, name)) for name in parameter_names)
        return f"{type(self).__name__}({parameters})"
