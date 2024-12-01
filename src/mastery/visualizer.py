from typing import Dict, List
from .models import Problem
from .models.progress import UserProgress
from .difficulty import DifficultyManager


class LearningPathVisualizer:
    def __init__(self):
        self.difficulty_manager = DifficultyManager()

    def get_topic_progress(self, user_id: str) -> Dict[str, Dict]:
        """Get detailed progress for each topic"""
        progress = {}

        for topic in self.difficulty_manager.topic_prerequisites.keys():
            # Get all problems attempted in this topic
            attempts = (UserProgress.query
                        .join(Problem)
                        .filter(
                            UserProgress.user_id == user_id,
                            Problem.topic == topic
                        ).all())

            total_problems = Problem.query.filter_by(topic=topic).count()
            solved_problems = sum(1 for a in attempts if a.solved)

            progress[topic] = {
                "total_problems": total_problems,
                "attempted": len(attempts),
                "solved": solved_problems,
                "completion_rate": solved_problems / total_problems if total_problems else 0,
                "available": topic in self.difficulty_manager.get_available_topics(user_id),
                "prerequisites_met": all(
                    prereq in progress and progress[prereq]["completion_rate"] >= 0.7
                    for prereq in self.difficulty_manager.topic_prerequisites[topic]
                )
            }

        return progress

    def get_learning_path(self, user_id: str) -> List[Dict]:
        """Get ordered list of topics with dependencies"""
        topic_progress = self.get_topic_progress(user_id)
        learning_path = []

        def add_prerequisites(topic: str, path: List[Dict]):
            """Recursively add prerequisites to path"""
            for prereq in self.difficulty_manager.topic_prerequisites[topic]:
                if not any(p["topic"] == prereq for p in path):
                    add_prerequisites(prereq, path)
                    path.append({
                        "topic": prereq,
                        "status": topic_progress[prereq]
                    })

        # Build path starting with available topics
        available_topics = self.difficulty_manager.get_available_topics(
            user_id)
        for topic in available_topics:
            if not any(p["topic"] == topic for p in learning_path):
                add_prerequisites(topic, learning_path)
                learning_path.append({
                    "topic": topic,
                    "status": topic_progress[topic]
                })

        return learning_path
