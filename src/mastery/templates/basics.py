from typing import Dict, Any
from .base import ProblemTemplate


class BasicsProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        return {
            "description": "Write a function that converts temperature from Celsius to Fahrenheit",
            "test_cases": [
                {"input": "celsius_to_fahrenheit(0)", "expected": 32.0},
                {"input": "celsius_to_fahrenheit(100)", "expected": 212.0}
            ],
            "starter_code": "def celsius_to_fahrenheit(celsius):\n    # Your code here\n    pass",
            "solution": "def celsius_to_fahrenheit(celsius):\n    return (celsius * 9/5) + 32"
        }
