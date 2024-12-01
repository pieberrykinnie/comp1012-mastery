from mastery.templates import ProblemTemplate, BasicsProblemTemplate


def test_base_template():
    template = ProblemTemplate("BASICS", 1)
    problem = template.generate()
    assert "description" in problem
    assert "test_cases" in problem
    assert "starter_code" in problem
    assert "solution" in problem


def test_basics_template():
    template = BasicsProblemTemplate("BASICS", 1)
    problem = template.generate()
    assert problem["description"] != ""
    assert len(problem["test_cases"]) > 0
    assert problem["starter_code"] != ""
    assert problem["solution"] != ""
