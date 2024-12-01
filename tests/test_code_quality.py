from mastery.code_quality import CodeQualityChecker


def test_indentation():
    checker = CodeQualityChecker()
    # Test missing indentation after colon
    code = """def test_function():
x = 1"""  # No indentation where it should be

    results = checker.analyze_code(code)
    assert any("expected an indented block" in msg.lower()
               for msg in results["errors"])


def test_naming_conventions():
    checker = CodeQualityChecker()
    code = """
def testFunction():
    TestVar = 42
    return TestVar
"""
    results = checker.analyze_code(code)
    assert any("must be lowercase with underscores" in msg
               for msg in results["errors"])


def test_operator_spacing():
    checker = CodeQualityChecker()
    code = """
def calc():
    x=1+2
    y = 3*4
    return x+y
"""
    results = checker.analyze_code(code)
    assert any("Missing spaces around" in msg for msg in results["errors"])


def test_docstring_requirement():
    checker = CodeQualityChecker()
    code = """
def test_function():
    x = 1
    return x
"""
    results = checker.analyze_code(code)
    assert any("must have a docstring" in msg for msg in results["errors"])


def test_import_placement():
    checker = CodeQualityChecker()
    code = """
def test_function():
    import math
    return math.pi
"""
    results = checker.analyze_code(code)
    assert any(
        "imports must be at the top" in msg for msg in results["errors"])
