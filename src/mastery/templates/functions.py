from typing import Dict, Any
from .base import ProblemTemplate


class FunctionProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        if self.difficulty == 1:
            return {
                "description": "Write a function that calculates the factorial of a number using iteration",
                "test_cases": [
                    {"input": "factorial(5)", "expected": 120},
                    {"input": "factorial(0)", "expected": 1},
                    {"input": "factorial(3)", "expected": 6}
                ],
                "starter_code": "def factorial(n):\n    # Your code here\n    pass",
                "solution": "def factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result"
            }
        elif self.difficulty == 2:
            return {
                "description": "Write a function that computes the sum of a geometric series: 1 + r + r^2 + ... + r^n",
                "test_cases": [
                    # 1 + 2 + 4 + 8 = 15
                    {"input": "geometric_sum(2, 3)", "expected": 15},
                    # 1 + 3 + 9 = 13
                    {"input": "geometric_sum(3, 2)", "expected": 13},
                    # 1 + 1 + 1 + 1 + 1 = 5
                    {"input": "geometric_sum(1, 4)", "expected": 5}
                ],
                "starter_code": "def geometric_sum(r, n):\n    # Your code here\n    pass",
                "solution": "def geometric_sum(r, n):\n    total = 0\n    for i in range(n + 1):\n        total += r ** i\n    return total"
            }
