from mastery.templates.numerical import NumericalProblemTemplate


def test_numerical_template_difficulty_1():
    template = NumericalProblemTemplate("BASICS", 1)
    problem = template.generate()
    assert "circle_area" in problem["starter_code"]
    assert len(problem["test_cases"]) == 2
    assert problem["description"] != ""


def test_numerical_template_difficulty_2():
    template = NumericalProblemTemplate("BASICS", 2)
    problem = template.generate()
    assert "fahrenheit_to_celsius" in problem["starter_code"]
    assert len(problem["test_cases"]) == 2
    assert problem["description"] != ""
