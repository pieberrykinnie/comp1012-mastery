from typing import Dict, Any
from .base import ProblemTemplate


class RandomProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        if self.difficulty == 1:
            return {
                "description": "Write a function that simulates rolling a six-sided die n times and returns the count of each number",
                "test_cases": [
                    {
                        "input": "verify_dice_simulation(dice_count(1000))",
                        "expected": True
                    },
                    {
                        "input": "len(dice_count(100))",
                        "expected": 6
                    }
                ],
                "starter_code": "import random\n\ndef dice_count(n):\n    # Your code here\n    pass",
                "solution": """import random

def dice_count(n):
    counts = [0] * 6
    for _ in range(n):
        roll = random.randint(1, 6)
        counts[roll-1] += 1
    return counts"""
            }
        elif self.difficulty == 2:
            return {
                "description": "Write a function that simulates a random walk of n steps, returning the final position",
                "test_cases": [
                    {
                        "input": "verify_random_walk(random_walk(1000))",
                        "expected": True
                    },
                    {
                        "input": "isinstance(random_walk(100), int)",
                        "expected": True
                    }
                ],
                "starter_code": "import random\n\ndef random_walk(n):\n    # Your code here\n    pass",
                "solution": """import random

def random_walk(n):
    position = 0
    for _ in range(n):
        step = random.choice([-1, 1])
        position += step
    return position"""
            }
