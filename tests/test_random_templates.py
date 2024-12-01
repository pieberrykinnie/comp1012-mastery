import pytest
from mastery.templates.random_numbers import RandomProblemTemplate


def verify_dice_simulation(counts):
    """Helper function to verify dice simulation results"""
    return (
        len(counts) == 6 and
        all(isinstance(x, int) for x in counts) and
        all(x >= 0 for x in counts)
    )


def verify_random_walk(position):
    """Helper function to verify random walk results"""
    return isinstance(position, int)


@pytest.fixture(autouse=True)
def add_verify_functions():
    """Add verification functions to globals"""
    globals()['verify_dice_simulation'] = verify_dice_simulation
    globals()['verify_random_walk'] = verify_random_walk


def test_random_template_difficulty_1():
    template = RandomProblemTemplate("RANDOM", 1)
    problem = template.generate()
    assert "dice_count" in problem["starter_code"]
    assert "random" in problem["solution"].lower()
    assert len(problem["test_cases"]) == 2

    # Test actual function execution
    exec(problem["solution"], globals())
    result = eval(problem["test_cases"][0]["input"])
    assert result == problem["test_cases"][0]["expected"]


def test_random_template_difficulty_2():
    template = RandomProblemTemplate("RANDOM", 2)
    problem = template.generate()
    assert "random_walk" in problem["starter_code"]
    assert "random" in problem["solution"].lower()
    assert len(problem["test_cases"]) == 2

    # Test actual function execution
    exec(problem["solution"], globals())
    result = eval(problem["test_cases"][1]["input"])
    assert result == problem["test_cases"][1]["expected"]
