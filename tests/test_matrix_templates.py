import numpy as np
from mastery.templates.matrices import MatrixProblemTemplate


def test_matrix_template_difficulty_1():
    template = MatrixProblemTemplate("MATRICES", 1)
    problem = template.generate()
    assert "matrix_transpose" in problem["starter_code"]
    assert len(problem["test_cases"]) == 2
    assert "numpy" in problem["solution"].lower()

    # Test actual matrix operations
    exec(problem["solution"], globals())
    result = eval(problem["test_cases"][0]["input"])
    expected = problem["test_cases"][0]["expected"]
    assert np.array_equal(result, expected)


def test_matrix_template_difficulty_2():
    template = MatrixProblemTemplate("MATRICES", 2)
    problem = template.generate()
    assert "matrix_multiply" in problem["starter_code"]
    assert len(problem["test_cases"]) == 2
    assert "numpy" in problem["solution"].lower()

    # Test actual matrix operations
    exec(problem["solution"], globals())
    result = eval(problem["test_cases"][0]["input"])
    expected = problem["test_cases"][0]["expected"]
    assert np.array_equal(result, expected)
