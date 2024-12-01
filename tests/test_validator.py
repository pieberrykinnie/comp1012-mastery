import pytest
from mastery.validator import ProblemValidator


def test_simple_arithmetic():
    validator = ProblemValidator()
    code = "def add(a, b): return a + b"
    test_cases = [
        {"input": "add(2, 3)", "expected": 5},
        {"input": "add(-1, 1)", "expected": 0}
    ]
    assert validator.validate_solution(code, test_cases)


def test_invalid_syntax():
    validator = ProblemValidator()
    code = "def add(a, b): return a +"  # Invalid syntax
    test_cases = [{"input": "add(2, 3)", "expected": 5}]
    assert not validator.validate_solution(code, test_cases)
