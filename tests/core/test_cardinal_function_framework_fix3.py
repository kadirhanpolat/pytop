from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_cardinal_function_framework_definitions_are_explicit_fix3():
    chapter = _read("manuscript/volume_2/chapters/29_cardinal_functions_framework.tex")
    for token in (
        "Beş temel fonksiyon için okuma sözlüğü",
        "Ağırlık",
        "Yoğunluk",
        "Karakter",
        "Lindelöf sayısı",
        "Hücresellik",
        "Noktasal invariant ile küresel invariant ayrımı",
    ):
        assert token in chapter


def test_cardinal_function_framework_examples_are_safe_and_comparative_fix3():
    chapter = _read("manuscript/volume_2/chapters/29_cardinal_functions_framework.tex")
    for token in (
        "Sonlu ayrık uzay",
        "Güvenli metrik örnek",
        "İkinci sayılabilir örnek",
        "Kardinal fonksiyonları yalnız $|X|$ ile özdeşleştirmek yanlıştır",
    ):
        assert token in chapter


def test_cardinal_function_framework_examples_bank_records_fix3_tasks():
    examples = _read("examples_bank/cardinal_functions_framework_examples.md")
    for token in (
        "CFF-FIX3-01",
        "finite discrete space",
        "safe metric second-countable example",
        "pointwise/global warning",
        "invariant comparison warning",
    ):
        assert token in examples


def test_cardinal_function_framework_notebooks_parse_as_json_fix3():
    for rel in (
        "notebooks/exploration/22_cardinal_functions_framework.ipynb",
        "notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb",
    ):
        data = json.loads(_read(rel))
        assert isinstance(data, dict)
        assert "cells" in data
