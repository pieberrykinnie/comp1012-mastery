from typing import Dict, List
from .code_quality import CodeQualityChecker


class StyleFeedback:
    def __init__(self):
        self.checker = CodeQualityChecker()

    def analyze_style(self, code: str) -> Dict[str, List[str]]:
        """Analyze code style and provide COMP 1012-specific feedback"""
        quality_results = self.checker.analyze_code(code)

        feedback = {
            "spacing": [],
            "naming": [],
            "documentation": [],
            "structure": []
        }

        # Check operator spacing
        for msg in quality_results["errors"]:
            if "operator" in msg.lower():
                feedback["spacing"].append(
                    "Add spaces around operators for better readability"
                )

        # Check naming conventions
        for msg in quality_results["errors"]:
            if "must be lowercase" in msg.lower():
                feedback["naming"].append(
                    "Use lowercase with underscores for variable and function names"
                )

        # Check documentation
        for msg in quality_results["errors"]:
            if "docstring" in msg.lower():
                feedback["documentation"].append(
                    "Add docstrings to explain function purpose and parameters"
                )

        return feedback
