import pytest
from datetime import datetime, timedelta
from mastery.recommender import ProblemRecommender
from mastery.models import db, Problem
from mastery.models.progress import UserProgress


def test_get_recommendations(app):
    with app.app_context():
        # Create test problems
        problems = []
        for i in range(3):
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

        # Create progress records
        progress = UserProgress(
            user_id="test_user",
            problem_id=problems[0].id,
            attempts=2,
            solved=False,
            last_attempt=datetime.utcnow()
        )
        db.session.add(progress)
        db.session.commit()

        recommender = ProblemRecommender()
        recommendations = recommender.get_recommendations("test_user", count=2)

        assert len(recommendations) <= 2
        assert all(isinstance(r["problem_id"], int) for r in recommendations)
        assert all(isinstance(r["reason"], str) for r in recommendations)


def test_recommendations_with_no_history(app):
    with app.app_context():
        # Create test problems
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

        recommender = ProblemRecommender()
        recommendations = recommender.get_recommendations("new_user")

        assert len(recommendations) <= 3  # Default count
        # Should start with easiest
        assert all(r["difficulty"] == 1 for r in recommendations)
