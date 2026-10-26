"""Обработка JSON-справочников из configs"""

import logging
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from src.readers import get_fields_from_json

FIELD_ALIASES_PATH = Path(__file__).resolve().parent.parent / "configs" / "field_aliases.json"

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("fields")
logger.setLevel(logging.DEBUG)
logger.propagate = False

file_handler = logging.FileHandler(
    LOG_DIR / "fields.log",
    mode="w",
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def _load_field_aliases() -> dict[str, list[str]]:
    """Загрузить и проверить справочник названий полей транзакций."""
    field_aliases = load_fields(FIELD_ALIASES_PATH)

    if not isinstance(field_aliases, dict):
        logger.error(
            "Не удалось загрузить справочник полей из %s: ожидался словарь, получено %s",
            FIELD_ALIASES_PATH,
            type(field_aliases).__name__,
        )
        return {}

    aliases_are_valid = all(
        isinstance(field_name, str) and isinstance(paths, list) and all(isinstance(path, str) for path in paths)
        for field_name, paths in field_aliases.items()
    )
    if not aliases_are_valid:
        logger.error("Справочник полей %s имеет некорректную структуру", FIELD_ALIASES_PATH)
        return {}

    logger.info("Справочник полей успешно загружен: %d полей", len(field_aliases))
    return cast(dict[str, list[str]], field_aliases)


def get_by_path(item: Mapping[str, Any], path: str) -> Any:
    """Получить значение по буквальному ключу или вложенному пути.

    Буквальный ключ имеет приоритет: для пути ``currency.code`` сначала
    проверяется ключ с таким полным именем, а затем вложенная структура
    ``{"currency": {"code": ...}}``.

    Raises:
        KeyError: Если указанный путь отсутствует.
    """
    try:
        return item[path]
    except KeyError:
        logger.debug("Буквальный ключ %r не найден", path)

    value: Any = item

    try:
        for key in path.split("."):
            value = value[key]
    except (KeyError, TypeError) as error:
        logger.debug("Вложенный путь %r не найден", path)
        logger.error(
            "Путь %r не найден: %s",
            path,
            error,
        )
        raise KeyError(path) from error

    return value


def get_field_value(
    transaction: Mapping[str, Any],
    field_name: str,
    field_aliases: Mapping[str, list[str]],
) -> Any:
    """Найти значение поля транзакции по первому доступному `aliase`.

    Returns:
        Значение первого найденного поля или пустой список, если поле
        отсутствует в справочнике либо транзакции.
    """
    try:
        paths = field_aliases[field_name]
    except KeyError as error:
        logger.error(
            "Поле %s отсутствует в справочнике: %s",
            field_name,
            error,
        )
        return []

    for path in paths:
        try:
            return get_by_path(transaction, path)
        except KeyError:
            continue

    logger.error("Поле %s отсутствует в транзакции", field_name)
    return []


def load_fields(file_path: str | Path) -> Any:
    """Загрузить справочник путей к полям."""
    data = get_fields_from_json(file_path)
    return data
