from typing import Dict, List
from datetime import datetime, timedelta
from .models import Problem
from .models.progress import UserProgress
from .visualizer import LearningPathVisualizer
from .analytics import ProgressAnalytics


class ReportGenerator:
    def __init__(self):
        self.visualizer = LearningPathVisualizer()
        self.analytics = ProgressAnalytics()

    def generate_student_report(self, user_id: str) -> Dict:
        """Generate comprehensive student progress report"""
        learning_path = self.visualizer.get_learning_path(user_id)
        stats = self.analytics.get_user_stats(user_id)
        weekly_progress = self.analytics.get_weekly_progress(user_id)

        # Calculate time spent per topic
        topic_time = {}
        progress_records = UserProgress.query.filter_by(user_id=user_id).all()
        for record in progress_records:
            topic = record.problem.topic
            if topic not in topic_time:
                topic_time[topic] = {
                    "attempts": 0,
                    "problems_attempted": set(),
                    "problems_solved": set()
                }
            topic_time[topic]["attempts"] += record.attempts
            topic_time[topic]["problems_attempted"].add(record.problem_id)
            if record.solved:
                topic_time[topic]["problems_solved"].add(record.problem_id)

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "overall_stats": stats,
            "weekly_progress": weekly_progress,
            "learning_path": learning_path,
            "topic_statistics": {
                topic: {
                    "total_attempts": data["attempts"],
                    "unique_problems_attempted": len(data["problems_attempted"]),
                    "problems_solved": len(data["problems_solved"]),
                    "success_rate": len(data["problems_solved"]) / len(data["problems_attempted"])
                    if data["problems_attempted"] else 0
                }
                for topic, data in topic_time.items()
            }
        }

    def generate_class_report(self, user_ids: List[str]) -> Dict:
        """Generate aggregate class progress report"""
        class_stats = {
            "total_students": len(user_ids),
            "active_students": 0,  # Students with attempts in last week
            "topic_completion": {},
            "difficulty_distribution": {i: 0 for i in range(1, 6)},
            "weekly_activity": {}
        }

        one_week_ago = datetime.utcnow() - timedelta(days=7)

        for user_id in user_ids:
            # Check recent activity
            recent_activity = (UserProgress.query
                               .filter_by(user_id=user_id)
                               .filter(UserProgress.last_attempt >= one_week_ago)
                               .first())

            if recent_activity:
                class_stats["active_students"] += 1

            # Get user's progress
            progress = self.visualizer.get_topic_progress(user_id)

            # Update topic completion stats
            for topic, status in progress.items():
                if topic not in class_stats["topic_completion"]:
                    class_stats["topic_completion"][topic] = {
                        "completed": 0,
                        "in_progress": 0,
                        "not_started": 0
                    }

                if status["completion_rate"] >= 0.8:
                    class_stats["topic_completion"][topic]["completed"] += 1
                elif status["completion_rate"] > 0:
                    class_stats["topic_completion"][topic]["in_progress"] += 1
                else:
                    class_stats["topic_completion"][topic]["not_started"] += 1

        return class_stats
