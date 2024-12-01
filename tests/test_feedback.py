from datetime import datetime, timedelta
from mastery.feedback import FeedbackGenerator
from mastery.models import db, Problem
from mastery.models.progress import UserProgress


def test_generate_feedback(app):
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

        # Add progress with multiple attempts
        progress = UserProgress(
            user_id="test_user",
            problem_id=problem.id,
            attempts=4,
            solved=False,
            last_attempt=datetime.utcnow()
        )
        db.session.add(progress)
        db.session.commit()

        generator = FeedbackGenerator()
        feedback = generator.generate_feedback("test_user")

        assert "overall_progress" in feedback
        assert "topic_feedback" in feedback
        assert "suggested_actions" in feedback
        assert "BASICS" in feedback["topic_feedback"]
        assert len(feedback["suggested_actions"]) > 0


def test_feedback_with_no_attempts(app):
    with app.app_context():
        generator = FeedbackGenerator()
        feedback = generator.generate_feedback("new_user")

        assert "overall_progress" in feedback
        assert "topic_feedback" in feedback
        assert "suggested_actions" in feedback
        assert len(feedback["topic_feedback"]) == 0
