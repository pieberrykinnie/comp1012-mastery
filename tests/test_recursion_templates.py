from mastery.templates.recursion import RecursionProblemTemplate


def test_recursion_template_difficulty_1():
    template = RecursionProblemTemplate("RECURSION", 1)
    problem = template.generate()
    assert "factorial" in problem["starter_code"]
    assert len(problem["test_cases"]) == 3

    # Test actual function execution
    exec(problem["solution"], globals())
    result = eval(problem["test_cases"][0]["input"])
    assert result == problem["test_cases"][0]["expected"]


def test_recursion_template_difficulty_2():
    template = RecursionProblemTemplate("RECURSION", 2)
    problem = template.generate()
    assert "fibonacci" in problem["starter_code"]
    assert len(problem["test_cases"]) == 3

    # Test actual function execution
    exec(problem["solution"], globals())
    result = eval(problem["test_cases"][0]["input"])
    assert result == problem["test_cases"][0]["expected"]
