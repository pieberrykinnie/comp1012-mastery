from typing import Dict, Any
from .base import ProblemTemplate


class RecursionProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        if self.difficulty == 1:
            return {
                "description": "Write a recursive function that calculates the factorial of a number",
                "test_cases": [
                    {"input": "factorial(5)", "expected": 120},
                    {"input": "factorial(0)", "expected": 1},
                    {"input": "factorial(3)", "expected": 6}
                ],
                "starter_code": "def factorial(n):\n    # Your code here\n    pass",
                "solution": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)"""
            }
        elif self.difficulty == 2:
            return {
                "description": "Write a recursive function that calculates the nth Fibonacci number",
                "test_cases": [
                    {"input": "fibonacci(6)", "expected": 8},
                    {"input": "fibonacci(1)", "expected": 1},
                    {"input": "fibonacci(7)", "expected": 13}
                ],
                "starter_code": "def fibonacci(n):\n    # Your code here\n    pass",
                "solution": """def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)"""
            }
