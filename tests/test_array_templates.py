from mastery.templates.arrays import ArrayProblemTemplate


def test_array_template_difficulty_1():
    template = ArrayProblemTemplate("ARRAYS", 1)
    problem = template.generate()
    assert "array_mean" in problem["starter_code"]
    assert len(problem["test_cases"]) == 2
    assert "numpy" in problem["solution"].lower()


def test_array_template_difficulty_2():
    template = ArrayProblemTemplate("ARRAYS", 2)
    problem = template.generate()
    assert "above_mean" in problem["starter_code"]
    assert len(problem["test_cases"]) == 2
    assert "np.mean" in problem["solution"]
