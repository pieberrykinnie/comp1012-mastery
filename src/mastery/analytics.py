from typing import Dict, List
from datetime import datetime, timedelta
from .models import db
from .models.progress import UserProgress


class ProgressAnalytics:
    def get_user_stats(self, user_id: str) -> Dict:
        """Get overall statistics for a user"""
        progress = UserProgress.query.filter_by(user_id=user_id).all()

        total_attempts = sum(p.attempts for p in progress)
        problems_solved = sum(1 for p in progress if p.solved)

        return {
            "total_attempts": total_attempts,
            "problems_solved": problems_solved,
            "completion_rate": problems_solved / len(progress) if progress else 0
        }

    def get_weekly_progress(self, user_id: str) -> List[Dict]:
        """Get user progress organized by week"""
        one_week_ago = datetime.utcnow() - timedelta(days=7)

        recent_progress = (UserProgress.query
                           .filter_by(user_id=user_id)
                           .filter(UserProgress.last_attempt >= one_week_ago)
                           .all())

        daily_stats = {}
        for progress in recent_progress:
            day = progress.last_attempt.date()
            if day not in daily_stats:
                daily_stats[day] = {"attempts": 0, "solved": 0}
            daily_stats[day]["attempts"] += progress.attempts
            if progress.solved:
                daily_stats[day]["solved"] += 1

        return [
            {
                "date": day.isoformat(),
                "attempts": stats["attempts"],
                "solved": stats["solved"]
            }
            for day, stats in sorted(daily_stats.items())
        ]
