from mastery.visualizer import LearningPathVisualizer
from mastery.models import db, Problem
from mastery.models.progress import UserProgress


def test_get_topic_progress(app):
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

        # Create progress record
        progress = UserProgress(
            user_id="test_user",
            problem_id=problem.id,
            attempts=1,
            solved=True
        )
        db.session.add(progress)
        db.session.commit()

        visualizer = LearningPathVisualizer()
        topic_progress = visualizer.get_topic_progress("test_user")

        assert "BASICS" in topic_progress
        assert topic_progress["BASICS"]["total_problems"] == 1
        assert topic_progress["BASICS"]["solved"] == 1
        assert topic_progress["BASICS"]["completion_rate"] == 1.0


def test_get_learning_path(app):
    with app.app_context():
        # Create test problems for multiple topics
        problems = [
            Problem(
                topic="BASICS",
                week=1,
                difficulty=1,
                description="Basics problem",
                test_cases=[],
                starter_code=""
            ),
            Problem(
                topic="STRINGS_IO",
                week=2,
                difficulty=1,
                description="Strings problem",
                test_cases=[],
                starter_code=""
            )
        ]
        db.session.add_all(problems)
        db.session.commit()

        # Add progress for BASICS
        progress = UserProgress(
            user_id="test_user",
            problem_id=problems[0].id,
            attempts=1,
            solved=True
        )
        db.session.add(progress)
        db.session.commit()

        visualizer = LearningPathVisualizer()
        learning_path = visualizer.get_learning_path("test_user")

        assert len(learning_path) > 0
        # Should start with basics
        assert learning_path[0]["topic"] == "BASICS"
        assert learning_path[0]["status"]["completion_rate"] == 1.0
