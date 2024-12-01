import pytest
from mastery.models import Problem
from mastery.models.progress import UserProgress


def test_problem_table_creation():
    assert hasattr(Problem, 'id')
    assert hasattr(Problem, 'topic')
    assert hasattr(Problem, 'difficulty')
    assert hasattr(Problem, 'description')
    assert hasattr(Problem, 'test_cases')
    assert hasattr(Problem, 'starter_code')
    assert hasattr(Problem, 'created_at')


def test_user_progress_table_creation():
    assert hasattr(UserProgress, 'id')
    assert hasattr(UserProgress, 'user_id')
    assert hasattr(UserProgress, 'problem_id')
    assert hasattr(UserProgress, 'attempts')
    assert hasattr(UserProgress, 'solved')
    assert hasattr(UserProgress, 'last_attempt')
