import types
import sys
from unittest.mock import MagicMock

if "tabulate" not in sys.modules:
    mock_tabulate = types.ModuleType("tabulate")
    mock_tabulate.tabulate = MagicMock(return_value = "TABLE")
    sys.modules["tabulate"] = mock_tabulate

import pytest
import csv
from project import *

def test_parse_year_month():
    assert parse_year_month("2025, 12") == (2025, 12)
    assert parse_year_month("2025, 1") == (2025, 1)

@pytest.mark.parametrize("invalid_input", ["2025 12", "2025-12", "2025 december"])
def test_parse_year_month_invalid(invalid_input):
    with pytest.raises(ValueError):
        parse_year_month(invalid_input)

    with pytest.raises(ValueError):
        parse_year_month("2025, 13")

def test_valid_date():
    assert valid_date(2024, 2, 29) is True #leap year
    assert valid_date(2025, 2, 29) is False
    assert valid_date(2025, 12, "abd") is False

def test_add_entry_to_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    path = get_file(2025, 12)
    add_entry_to_csv(path, 2025, 12, 25, 1000, "Food")

    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.reader(file))
    
    assert rows[-1] == ["2025", "12", "25","1000", "Food"]

def test_calculate_stats(tmp_path):
    path = tmp_path/"data.csv"
    with path.open("w", encoding="utf-8", newline="") as file:
        w = csv.writer(file)
        w.writerow(["Year", "Month", "Day", "Amount", "Category"])
        w.writerow([2025, 12, 1, "1000", "food"])
        w.writerow([2025, 12, 2, "2000", "Food"])
        w.writerow([2025, 12, 3, "3000", "school"])
        
    total, cats = calculate_stats(path)

    assert total == pytest.approx(6000)
    assert cats["Food"] == pytest.approx(3000)
    assert cats["School"] == pytest.approx(3000)
