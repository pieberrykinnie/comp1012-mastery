import pytest
from mastery.repository import ProblemRepository
from mastery.models import Problem


def test_repository_creation():
    repo = ProblemRepository()
    assert repo is not None
    assert "BASICS" in repo.template_map


def test_problem_creation(app):
    with app.app_context():
        repo = ProblemRepository()
        problem = repo.create_problem("BASICS", 1)
        assert isinstance(problem, Problem)
        assert problem.id is not None
        assert problem.topic == "BASICS"
        assert problem.difficulty == 1
        assert problem.starter_code is not None


def test_get_problems_by_topic(app):
    with app.app_context():
        repo = ProblemRepository()
        repo.create_problem("BASICS", 1)
        repo.create_problem("BASICS", 2)

        problems = repo.get_problems_by_topic("BASICS")
        assert len(problems) == 2
        assert all(p.topic == "BASICS" for p in problems)


def test_get_problem_by_id(app):
    with app.app_context():
        repo = ProblemRepository()
        created = repo.create_problem("BASICS", 1)

        retrieved = repo.get_problem_by_id(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
