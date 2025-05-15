import pytest

import io
import sys
from main import read_csv_files, generate_payout_report

csv_content_1 = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60
"""

csv_content_2 = """department,id,email,name,hours_worked,rate
HR,101,grace@example.com,Grace Lee,160,45
Marketing,102,henry@example.com,Henry Martin,150,35
HR,103,ivy@example.com,Ivy Clark,158,38
"""

csv_content_3 = """email,name,department,hours_worked,salary,id
karen@example.com,Karen White,Sales,165,50,201
liam@example.com,Liam Harris,HR,155,42,202
mia@example.com,Mia Young,Sales,160,37,203
"""


def fake_open(file_path):
    if file_path == 'file1.csv':
        return io.StringIO(csv_content_1)
    elif file_path == 'file2.csv':
        return io.StringIO(csv_content_2)
    elif file_path == 'file3.csv':
        return io.StringIO(csv_content_3)
    else:
        raise FileNotFoundError(f"No such file: {file_path}")


@pytest.fixture(autouse=True)
def patch_open(monkeypatch):
    monkeypatch.setattr("builtins.open", fake_open)


def test_read_csv_files():
    files = ['file1.csv', 'file2.csv', 'file3.csv']
    data = read_csv_files(files)
    assert len(data) >= 8


def test_generate_payout_report(capsys):
    data = read_csv_files(['file1.csv', 'file2.csv', 'file3.csv'])

    generate_payout_report(data)

    captured = capsys.readouterr()
    output = captured.out

    assert "Alice Johnson" in output
    assert "Bob Smith" in output
    assert "Carol Williams" in output

def test_salary_calculation_with_missing_salary():
    csv_no_salary = """id,email,name,hours_worked,hourly_rate\n4,jane@example.com,Jane Doe,160,55"""

    def fake_open_single(file_path):
        return io.StringIO(csv_no_salary) if file_path == 'file4.csv' else fake_open(file_path)

    import builtins
    original_open = builtins.open
    builtins.open = fake_open_single

    try:
        data = read_csv_files(['file4.csv'])
        generate_payout_report(data)
        captured = capsys.readouterr()
        assert "Jane Doe" in captured.out
        assert "8800.00" in captured.out

    finally:
        builtins.open = original_open