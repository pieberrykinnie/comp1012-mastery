from typing import Dict, List
import random
from .constants import TOPICS


class ProblemGenerator:
    def __init__(self):
        self.problem_bank = {}

    def generate_problem(self, topic: str, difficulty: int) -> Dict:
        if topic not in TOPICS:
            raise ValueError(f"Invalid topic: {topic}")

        if difficulty not in range(1, 6):
            raise ValueError("Difficulty must be between 1 and 5")

        # Placeholder for actual problem generation
        return {
            "topic": topic,
            "difficulty": difficulty,
            "description": f"Practice problem for {topic}",
            "test_cases": []
        }
