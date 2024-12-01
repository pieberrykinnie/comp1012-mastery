from typing import Dict, Any
from . import ProblemTemplate


class NumericalProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        if self.difficulty == 1:
            return {
                "description": "Write a function that calculates the area of a circle given its radius",
                "test_cases": [
                    {"input": "circle_area(1.0)",
                     "expected": 3.141592653589793},
                    {"input": "circle_area(2.5)",
                     "expected": 19.634954084936208}
                ],
                "starter_code": "def circle_area(radius):\n    # Your code here\n    pass",
                "solution": "def circle_area(radius):\n    import math\n    return math.pi * radius ** 2"
            }
        elif self.difficulty == 2:
            return {
                "description": "Write a function that converts temperature from Fahrenheit to Celsius",
                "test_cases": [
                    {"input": "fahrenheit_to_celsius(32.0)", "expected": 0.0},
                    {"input": "fahrenheit_to_celsius(212.0)",
                     "expected": 100.0}
                ],
                "starter_code": "def fahrenheit_to_celsius(fahrenheit):\n    # Your code here\n    pass",
                "solution": "def fahrenheit_to_celsius(fahrenheit):\n    return (fahrenheit - 32) * 5/9"
            }
