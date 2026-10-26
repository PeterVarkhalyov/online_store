"""Тесты функций чтения JSON- и Excel-файлов."""

import json
from pathlib import Path

import pandas as pd
import pytest

from src import readers


@pytest.mark.parametrize(
    "data",
    [
        {"name": "Смартфоны"},
        [{"name": "Смартфоны"}, {"name": "Телевизоры"}],
    ],
)
def test_get_fields_from_json_reads_objects_and_arrays(tmp_path: Path, data: object) -> None:
    """JSON-объекты и массивы загружаются без преобразований."""
    file_path = tmp_path / "data.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    assert readers.get_fields_from_json(file_path) == data


def test_get_fields_from_json_returns_empty_list_for_invalid_data(tmp_path: Path) -> None:
    """Ошибочный JSON, скаляр и отсутствующий файл обрабатываются безопасно."""
    invalid_json_path = tmp_path / "invalid.json"
    invalid_json_path.write_text("{invalid", encoding="utf-8")
    scalar_path = tmp_path / "scalar.json"
    scalar_path.write_text('"строка"', encoding="utf-8")

    assert readers.get_fields_from_json(invalid_json_path) == []
    assert readers.get_fields_from_json(scalar_path) == []
    assert readers.get_fields_from_json(tmp_path / "missing.json") == []


def test_get_transactions_from_xls_skips_empty_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    """Полностью пустые строки Excel не попадают в результат."""
    data_frame = pd.DataFrame(
        [
            {"id": 1, "description": "Покупка"},
            {"id": None, "description": "   "},
        ]
    )

    def fake_read_excel(file_path: str | Path, sheet_name: str) -> pd.DataFrame:
        assert file_path == "operations.xlsx"
        assert sheet_name == "Отчет по операциям"
        return data_frame

    monkeypatch.setattr(readers.pd, "read_excel", fake_read_excel)

    result = readers.get_transactions_from_xls("operations.xlsx")

    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["description"] == "Покупка"


def test_get_transactions_from_xls_returns_empty_list_for_empty_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Пустой Excel-файл преобразуется в пустой список."""

    def fake_read_excel(file_path: str | Path, sheet_name: str) -> pd.DataFrame:
        return pd.DataFrame()

    monkeypatch.setattr(readers.pd, "read_excel", fake_read_excel)

    assert readers.get_transactions_from_xls("empty.xlsx") == []


def test_get_transactions_from_xls_returns_empty_list_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ошибка чтения Excel преобразуется в пустой список."""

    def raise_os_error(*args: object, **kwargs: object) -> pd.DataFrame:
        raise OSError("Файл недоступен")

    monkeypatch.setattr(readers.pd, "read_excel", raise_os_error)

    assert readers.get_transactions_from_xls("missing.xlsx") == []
