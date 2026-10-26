"""Тест запуска демонстрационного модуля."""

import runpy
from pathlib import Path

import pytest


def test_main_runs_without_errors(capsys: pytest.CaptureFixture[str]) -> None:
    """Весь код под защитой __main__ выполняется без исключений."""
    main_path = Path(__file__).resolve().parent.parent / "main.py"

    runpy.run_path(str(main_path), run_name="__main__")

    output = capsys.readouterr().out
    assert "Samsung Galaxy S23 Ultra" in output
    assert "Телевизоры" in output
