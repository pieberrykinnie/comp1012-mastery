import pytest
from datetime import datetime
from mastery.tracker import ProgressTracker
from mastery.models.progress import UserProgress


def test_record_first_attempt(app):
    with app.app_context():
        # Create a test problem first
        from mastery.repository import ProblemRepository
        repo = ProblemRepository()
        problem = repo.create_problem("BASICS", 1)

        tracker = ProgressTracker()
        result = tracker.record_attempt(
            "test_user",
            problem.id,
            "def celsius_to_fahrenheit(celsius):\n    return (celsius * 9/5) + 32"
        )

        assert result["correct"] == True
        assert result["attempts"] == 1


def test_multiple_attempts(app):
    with app.app_context():
        # Create a test problem
        from mastery.repository import ProblemRepository
        repo = ProblemRepository()
        problem = repo.create_problem("BASICS", 1)

        tracker = ProgressTracker()
        # First attempt - incorrect
        tracker.record_attempt(
            "test_user",
            problem.id,
            "def celsius_to_fahrenheit(celsius):\n    return celsius"
        )

        # Second attempt - correct
        result = tracker.record_attempt(
            "test_user",
            problem.id,
            "def celsius_to_fahrenheit(celsius):\n    return (celsius * 9/5) + 32"
        )

        assert result["correct"] == True
        assert result["attempts"] == 2


def test_get_user_progress(app):
    with app.app_context():
        # Create test problems
        from mastery.repository import ProblemRepository
        repo = ProblemRepository()
        problem1 = repo.create_problem("BASICS", 1)
        problem2 = repo.create_problem("BASICS", 2)

        tracker = ProgressTracker()
        tracker.record_attempt(
            "test_user", problem1.id, "def celsius_to_fahrenheit(celsius):\n    return (celsius * 9/5) + 32")
        tracker.record_attempt(
            "test_user", problem2.id, "def celsius_to_fahrenheit(celsius):\n    return celsius")

        progress = tracker.get_user_progress("test_user")
        assert len(progress) == 2
        assert all(isinstance(p["last_attempt"], datetime) for p in progress)
