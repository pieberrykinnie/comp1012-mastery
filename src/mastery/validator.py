import ast
from typing import Dict, Any


class ProblemValidator:
    def __init__(self):
        self.globals = {}
        self.locals = {}

    def validate_solution(self, code: str, test_cases: list[Dict[str, Any]]) -> bool:
        try:
            # Parse code to check for syntax errors
            ast.parse(code)

            # Execute student code
            exec(code, self.globals, self.locals)

            # Run test cases
            for test in test_cases:
                result = eval(test["input"], self.globals, self.locals)
                if result != test["expected"]:
                    return False
            return True
        except Exception:
            return False
