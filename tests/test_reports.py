from datetime import datetime, timedelta
from mastery.reports import ReportGenerator
from mastery.models import db, Problem
from mastery.models.progress import UserProgress


def test_generate_student_report(app):
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
            attempts=3,
            solved=True,
            last_attempt=datetime.utcnow()
        )
        db.session.add(progress)
        db.session.commit()

        generator = ReportGenerator()
        report = generator.generate_student_report("test_user")

        assert "generated_at" in report
        assert "overall_stats" in report
        assert "weekly_progress" in report
        assert "learning_path" in report
        assert "topic_statistics" in report
        assert "BASICS" in report["topic_statistics"]


def test_generate_class_report(app):
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

        # Add progress for multiple users
        users = ["user1", "user2"]
        for user_id in users:
            progress = UserProgress(
                user_id=user_id,
                problem_id=problem.id,
                attempts=1,
                solved=True,
                last_attempt=datetime.utcnow()
            )
            db.session.add(progress)
        db.session.commit()

        generator = ReportGenerator()
        report = generator.generate_class_report(users)

        assert report["total_students"] == 2
        assert report["active_students"] == 2
        assert "BASICS" in report["topic_completion"]
