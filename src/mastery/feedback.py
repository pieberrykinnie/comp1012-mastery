from typing import Dict, List
from datetime import datetime, timedelta
from .models import Problem
from .models.progress import UserProgress
from .analytics import ProgressAnalytics
from .recommender import ProblemRecommender


class FeedbackGenerator:
    def __init__(self):
        self.analytics = ProgressAnalytics()
        self.recommender = ProblemRecommender()

    def generate_feedback(self, user_id: str) -> Dict:
        """Generate personalized feedback based on student performance"""
        stats = self.analytics.get_user_stats(user_id)
        weekly_progress = self.analytics.get_weekly_progress(user_id)
        recommendations = self.recommender.get_recommendations(user_id)

        # Analyze recent performance
        recent_attempts = (UserProgress.query
                           .filter_by(user_id=user_id)
                           .filter(UserProgress.last_attempt >= datetime.utcnow() - timedelta(days=7))
                           .join(Problem)
                           .all())

        topic_feedback = {}
        for attempt in recent_attempts:
            topic = attempt.problem.topic
            if topic not in topic_feedback:
                topic_feedback[topic] = {
                    "attempts": 0,
                    "solved": 0,
                    "high_attempt_problems": []
                }

            topic_feedback[topic]["attempts"] += attempt.attempts
            if attempt.solved:
                topic_feedback[topic]["solved"] += 1
            if attempt.attempts > 3 and not attempt.solved:
                topic_feedback[topic]["high_attempt_problems"].append(
                    attempt.problem.id
                )

        return {
            "overall_progress": {
                "completion_rate": stats["completion_rate"],
                "recent_activity": len(weekly_progress),
                "recommendations": recommendations
            },
            "topic_feedback": topic_feedback,
            "suggested_actions": self._generate_suggestions(topic_feedback)
        }

    def _generate_suggestions(self, topic_feedback: Dict) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []

        for topic, feedback in topic_feedback.items():
            if feedback["attempts"] > 0:
                success_rate = feedback["solved"] / feedback["attempts"]
                if success_rate < 0.5:
                    suggestions.append(
                        f"Review {topic} fundamentals - success rate is below 50%"
                    )
                if feedback["high_attempt_problems"]:
                    suggestions.append(
                        f"Seek help with challenging {topic} problems"
                    )

        return suggestions
