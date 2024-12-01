from typing import List, Dict
from datetime import datetime, timedelta
from .models import Problem
from .models.progress import UserProgress
from .difficulty import DifficultyManager


class ProblemRecommender:
    def __init__(self):
        self.difficulty_manager = DifficultyManager()

    def get_recommendations(self, user_id: str, count: int = 3) -> List[Dict]:
        """Get personalized problem recommendations"""
        # Get available topics
        available_topics = self.difficulty_manager.get_available_topics(
            user_id)

        # Get recent activity
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        recent_progress = (UserProgress.query
                           .filter_by(user_id=user_id)
                           .filter(UserProgress.last_attempt >= one_week_ago)
                           .all())

        recommendations = []

        # Prioritize topics with recent unsuccessful attempts
        struggling_topics = set()
        for progress in recent_progress:
            if not progress.solved and progress.attempts >= 2:
                struggling_topics.add(progress.problem.topic)

        # Get problems from struggling topics first
        for topic in struggling_topics.intersection(available_topics):
            next_level = self.difficulty_manager.get_next_problem(
                user_id, topic)
            problems = Problem.query.filter_by(
                topic=topic,
                difficulty=next_level["difficulty"]
            ).all()

            if problems:
                recommendations.extend([{
                    "problem_id": p.id,
                    "topic": p.topic,
                    "difficulty": p.difficulty,
                    "reason": "Practice makes perfect! Keep working on this topic."
                } for p in problems[:count]])

        # Fill remaining slots with new topics
        remaining = count - len(recommendations)
        if remaining > 0:
            for topic in available_topics:
                if topic not in struggling_topics:
                    next_level = self.difficulty_manager.get_next_problem(
                        user_id, topic)
                    problems = Problem.query.filter_by(
                        topic=topic,
                        difficulty=next_level["difficulty"]
                    ).all()

                    if problems:
                        recommendations.extend([{
                            "problem_id": p.id,
                            "topic": p.topic,
                            "difficulty": p.difficulty,
                            "reason": "Try this new topic to expand your skills!"
                        } for p in problems[:remaining]])

                    if len(recommendations) >= count:
                        break

        return recommendations[:count]
