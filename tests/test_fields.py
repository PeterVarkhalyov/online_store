"""Тесты поиска значений по алиасам полей."""

from pathlib import Path
from typing import Any

import pytest

from src import fields


def test_get_by_path_prefers_literal_key() -> None:
    """Полный ключ имеет приоритет перед одноименным вложенным путем."""
    item = {
        "currency.code": "literal",
        "currency": {"code": "nested"},
    }

    assert fields.get_by_path(item, "currency.code") == "literal"


def test_get_by_path_reads_nested_value() -> None:
    """Значение извлекается из вложенной структуры."""
    item = {"currency": {"code": "RUB"}}

    assert fields.get_by_path(item, "currency.code") == "RUB"


def test_get_by_path_raises_key_error_for_missing_path() -> None:
    """Отсутствующий путь приводит к ожидаемому KeyError."""
    with pytest.raises(KeyError, match="currency.code"):
        fields.get_by_path({}, "currency.code")


def test_get_field_value_uses_first_available_alias() -> None:
    """Поиск переходит к следующему алиасу, если первый отсутствует."""
    item = {"product": {"name": "Iphone 15"}}
    aliases = {"name": ["name", "product.name"]}

    assert fields.get_field_value(item, "name", aliases) == "Iphone 15"


@pytest.mark.parametrize(
    ("field_name", "aliases"),
    [
        ("unknown", {"name": ["name"]}),
        ("name", {"name": ["name"]}),
    ],
)
def test_get_field_value_returns_empty_list_when_value_is_missing(
    field_name: str,
    aliases: dict[str, list[str]],
) -> None:
    """Отсутствующее поле или значение преобразуется в пустой список."""
    assert fields.get_field_value({}, field_name, aliases) == []


def test_load_fields_delegates_to_json_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    """Справочник загружается через get_fields_from_json."""
    expected = {"name": ["name"]}

    def fake_get_fields_from_json(file_path: str | Path) -> dict[str, list[str]]:
        assert file_path == "aliases.json"
        return expected

    monkeypatch.setattr(fields, "get_fields_from_json", fake_get_fields_from_json)

    assert fields.load_fields("aliases.json") == expected


@pytest.mark.parametrize("data", [[], {"name": "name"}, {1: ["name"]}])
def test_load_field_aliases_rejects_invalid_structure(monkeypatch: pytest.MonkeyPatch, data: Any) -> None:
    """Некорректный справочник алиасов преобразуется в пустой словарь."""
    monkeypatch.setattr(fields, "load_fields", lambda _: data)

    assert fields._load_field_aliases() == {}
