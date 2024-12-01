from typing import Dict, List
from .models import Problem
from .repository import ProblemRepository


class ContentManager:
    def __init__(self):
        self.repo = ProblemRepository()
        self.weeks = {
            1: {"topic": "BASICS", "subtopics": ["variables", "expressions", "operators"]},
            2: {"topic": "STRINGS_IO", "subtopics": ["string operations", "input", "output"]},
            3: {"topic": "CONTROL_FLOW", "subtopics": ["if statements", "while loops"]},
            4: {"topic": "COLLECTIONS", "subtopics": ["for loops", "files", "lists"]},
            5: {"topic": "DATA_STRUCTURES", "subtopics": ["lists", "sets", "dictionaries"]},
            6: {"topic": "FUNCTIONS", "subtopics": ["functions", "parameters"]},
            7: {"topic": "RANDOM", "subtopics": ["random module", "simulation"]},
            8: {"topic": "ARRAYS", "subtopics": ["numpy arrays", "array operations"]},
            9: {"topic": "MULTIDIM_ARRAYS", "subtopics": ["matrices", "matrix operations"]},
            10: {"topic": "OBJECTS", "subtopics": ["classes", "objects", "methods"]},
            11: {"topic": "RECURSION", "subtopics": ["recursive functions"]}
        }

    def get_week_content(self, week: int) -> Dict[str, List[Problem]]:
        if week not in self.weeks:
            raise ValueError(f"Invalid week number: {week}")

        topic = self.weeks[week]["topic"]
        problems = self.repo.get_problems_by_topic(topic)

        return {
            "topic": topic,
            "subtopics": self.weeks[week]["subtopics"],
            "problems": problems
        }
