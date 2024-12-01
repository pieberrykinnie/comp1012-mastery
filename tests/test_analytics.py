from datetime import datetime, timedelta
from mastery.analytics import ProgressAnalytics
from mastery.models.progress import UserProgress
from mastery.models import db, Problem


def test_get_user_stats(app):
    with app.app_context():
        # Create test data
        problem = Problem(
            topic="BASICS",
            week=1,
            difficulty=1,
            description="Test problem",
            test_cases=[],
            starter_code=""
        )
        db.session.add(problem)
        db.session.commit()

        progress = UserProgress(
            user_id="test_user",
            problem_id=problem.id,
            attempts=5,
            solved=True
        )
        db.session.add(progress)
        db.session.commit()

        analytics = ProgressAnalytics()
        stats = analytics.get_user_stats("test_user")

        assert stats["total_attempts"] == 5
        assert stats["problems_solved"] == 1
        assert stats["completion_rate"] == 1.0


def test_get_weekly_progress(app):
    with app.app_context():
        # Create multiple test problems instead of using the same one
        problems = []
        for i in range(7):
            problem = Problem(
                topic="BASICS",
                week=1,
                difficulty=1,
                description=f"Test problem {i}",
                test_cases=[],
                starter_code=""
            )
            db.session.add(problem)
            problems.append(problem)
        db.session.commit()

        # Add progress for last week using different problems
        for i, days_ago in enumerate(range(7)):
            progress = UserProgress(
                user_id="test_user",
                problem_id=problems[i].id,
                attempts=1,
                solved=True,
                last_attempt=datetime.utcnow() - timedelta(days=days_ago)
            )
            db.session.add(progress)
        db.session.commit()

        analytics = ProgressAnalytics()
        weekly_stats = analytics.get_weekly_progress("test_user")

        assert len(weekly_stats) > 0
        assert all(isinstance(day["date"], str) for day in weekly_stats)
        assert all(day["attempts"] > 0 for day in weekly_stats)
