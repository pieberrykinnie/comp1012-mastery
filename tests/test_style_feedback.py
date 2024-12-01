from mastery.style_feedback import StyleFeedback


def test_spacing_feedback():
    feedback = StyleFeedback()
    code = "x=1+2"
    results = feedback.analyze_style(code)
    assert any("spaces around operators" in msg
               for msg in results["spacing"])


def test_naming_feedback():
    feedback = StyleFeedback()
    code = "def testFunction():\n    pass"
    results = feedback.analyze_style(code)
    assert any("lowercase with underscores" in msg
               for msg in results["naming"])


def test_documentation_feedback():
    feedback = StyleFeedback()
    code = "def test_function():\n    pass"
    results = feedback.analyze_style(code)
    assert any("docstrings" in msg
               for msg in results["documentation"])
