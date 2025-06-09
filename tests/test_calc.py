import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from handlers.calc import safe_eval, format_result



@pytest.mark.parametrize("expr,expected", [
    ("2 + 2", 4),
    ("5 - 3", 2),
    ("2 * 3", 6),
    ("8 / 2", 4.0),
])
def test_safe_eval_basic(expr, expected):
    assert safe_eval(expr) == expected

@pytest.mark.parametrize("expr,expected", [
    ("sqrt(16)", 4.0),
    ("sin(pi/2)", 1.0),
    ("log(e)", 1.0),
])
def test_safe_eval_functions(expr, expected):
    assert pytest.approx(safe_eval(expr), rel=1e-5) == expected

@pytest.mark.parametrize("expr", [
    "2 + bad_function(3)",
    "2 + 'text'",
    "__import__('os').system('rm -rf /')",
])
def test_safe_eval_invalid(expr):
    with pytest.raises(ValueError):
        safe_eval(expr)

@pytest.mark.parametrize("value,expected", [
    (1000, "1 000"),
    (1234567, "1 234 567"),
    (3.1415926535, "3,1415926535"),
    (2.0, "2"),
])
def test_format_result(value, expected):
    assert format_result(value) == expected
