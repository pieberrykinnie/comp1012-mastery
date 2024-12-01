from typing import Dict, List
from .models import Problem
from .models.progress import UserProgress
from datetime import datetime, timedelta


class DifficultyManager:
    def __init__(self):
        self.topic_prerequisites = {
            "BASICS": [],
            "STRINGS_IO": ["BASICS"],
            "CONTROL_FLOW": ["BASICS", "STRINGS_IO"],
            "COLLECTIONS": ["CONTROL_FLOW"],
            "DATA_STRUCTURES": ["COLLECTIONS"],
            "FUNCTIONS": ["DATA_STRUCTURES"],
            "RANDOM": ["FUNCTIONS"],
            "ARRAYS": ["FUNCTIONS"],
            "MULTIDIM_ARRAYS": ["ARRAYS"],
            "OBJECTS": ["FUNCTIONS"],
            "RECURSION": ["FUNCTIONS"]
        }

    def get_available_topics(self, user_id: str) -> List[str]:
        """Get topics available to the user based on their progress"""
        completed_topics = set()
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            solved=True
        ).join(Problem).all()

        for p in progress:
            completed_topics.add(p.problem.topic)

        available = []
        for topic, prereqs in self.topic_prerequisites.items():
            if all(p in completed_topics for p in prereqs):
                available.append(topic)

        return available

    def get_next_problem(self, user_id: str, topic: str) -> Dict:
        """Get appropriate next problem based on user's progress"""
        progress = UserProgress.query.filter_by(
            user_id=user_id
        ).join(Problem).filter(
            Problem.topic == topic
        ).all()

        if not progress:
            return {"difficulty": 1, "week": 1}

        solved = sum(1 for p in progress if p.solved)
        total = len(progress)

        if solved / total >= 0.8:  # 80% success rate
            return {"difficulty": min(5, max(p.problem.difficulty for p in progress) + 1),
                    "week": max(p.problem.week for p in progress)}
        else:
            return {"difficulty": max(1, min(p.problem.difficulty for p in progress)),
                    "week": min(p.problem.week for p in progress)}
