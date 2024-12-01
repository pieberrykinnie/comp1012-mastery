import pytest
from mastery.difficulty import DifficultyManager
from mastery.models import db, Problem
from mastery.models.progress import UserProgress


def test_topic_prerequisites():
    manager = DifficultyManager()
    assert len(manager.topic_prerequisites) == 11
    assert manager.topic_prerequisites["BASICS"] == []
    assert "BASICS" in manager.topic_prerequisites["STRINGS_IO"]
    assert "FUNCTIONS" in manager.topic_prerequisites["RECURSION"]


def test_get_available_topics(app):
    with app.app_context():
        # Create test problems
        basics = Problem(
            topic="BASICS",
            week=1,
            difficulty=1,
            description="Test basics",
            test_cases=[],
            starter_code=""
        )
        strings = Problem(
            topic="STRINGS_IO",
            week=2,
            difficulty=1,
            description="Test strings",
            test_cases=[],
            starter_code=""
        )
        db.session.add_all([basics, strings])
        db.session.commit()

        # Create progress records
        progress = UserProgress(
            user_id="test_user",
            problem_id=basics.id,
            attempts=1,
            solved=True
        )
        db.session.add(progress)
        db.session.commit()

        manager = DifficultyManager()
        available = manager.get_available_topics("test_user")

        assert "BASICS" in available
        assert "STRINGS_IO" in available
        assert "CONTROL_FLOW" not in available


def test_get_next_problem(app):
    with app.app_context():
        # Create test problem
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

        # Test with no previous attempts
        manager = DifficultyManager()
        next_problem = manager.get_next_problem("test_user", "BASICS")
        assert next_problem["difficulty"] == 1
        assert next_problem["week"] == 1

        # Test with successful attempts
        progress = UserProgress(
            user_id="test_user",
            problem_id=problem.id,
            attempts=1,
            solved=True
        )
        db.session.add(progress)
        db.session.commit()

        next_problem = manager.get_next_problem("test_user", "BASICS")
        assert next_problem["difficulty"] == 2
