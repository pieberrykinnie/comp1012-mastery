import pytest
from mastery.models import Problem


def test_problem_creation():
    problem = Problem(
        topic="Numerical Computation",
        week=1,
        difficulty=1,
        description="Calculate the sum of two floating-point numbers",
        test_cases=[
            {"input": "2.5 + 3.5", "expected": 6.0},
            {"input": "-1.5 + 2.5", "expected": 1.0}
        ]
    )
    assert problem.topic == "Numerical Computation"
    assert problem.week == 1
    assert len(problem.test_cases) == 2
