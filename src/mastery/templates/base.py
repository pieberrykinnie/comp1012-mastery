from typing import Dict, Any


class ProblemTemplate:
    def __init__(self, topic: str, difficulty: int):
        self.topic = topic
        self.difficulty = difficulty

    def generate(self) -> Dict[str, Any]:
        return {
            "description": "",
            "test_cases": [],
            "starter_code": "",
            "solution": ""
        }
