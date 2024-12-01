import pytest
from mastery.generator import ProblemGenerator


def test_problem_generator_creation():
    generator = ProblemGenerator()
    assert generator is not None


def test_invalid_topic():
    generator = ProblemGenerator()
    with pytest.raises(ValueError):
        generator.generate_problem("INVALID_TOPIC", 1)


def test_invalid_difficulty():
    generator = ProblemGenerator()
    with pytest.raises(ValueError):
        generator.generate_problem("BASICS", 0)
    with pytest.raises(ValueError):
        generator.generate_problem("BASICS", 6)
