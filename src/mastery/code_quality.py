import ast
from typing import List, Dict
import re


class CodeQualityChecker:
    def __init__(self):
        self.style_rules = {
            "indentation": self._check_indentation,
            "naming": self._check_naming_conventions,
            "spacing": self._check_spacing,
            "docstring": self._check_docstring,
            "imports": self._check_imports
        }

    def analyze_code(self, code: str) -> Dict[str, List[str]]:
        """Analyze code according to COMP 1012 standards"""
        try:
            tree = ast.parse(code)
            issues = {
                "errors": [],
                "warnings": [],
                "suggestions": []
            }

            # Check indentation before parsing
            indent_issues = self._check_indentation(code)
            for severity, messages in indent_issues.items():
                issues[severity].extend(messages)

            # Apply other rules
            for rule_name, rule_checker in self.style_rules.items():
                if rule_name != "indentation":  # Already checked
                    rule_issues = rule_checker(tree, code)
                    for severity, messages in rule_issues.items():
                        issues[severity].extend(messages)

            return issues
        except SyntaxError as e:
            return {
                "errors": [f"Syntax error: {str(e)}"],
                "warnings": [],
                "suggestions": []
            }

    def _check_indentation(self, code: str) -> Dict[str, List[str]]:
        """Check for basic indentation presence"""
        issues = {"errors": [], "warnings": []}
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            if line.strip() and not line.startswith((' ', '\t')) and ':' in lines[i-2]:
                # Only check if indentation is missing after a colon
                issues["errors"].append(
                    f"Line {i}: Missing indentation after ':'"
                )

        return issues

    def _check_naming_conventions(self, tree: ast.AST, code: str) -> Dict[str, List[str]]:
        """Check COMP 1012 naming conventions"""
        issues = {"errors": [], "warnings": []}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Function names must be lowercase with underscores
                if not re.match(r'^[a-z][a-z0-9_]*$', node.name):
                    issues["errors"].append(
                        f"Function '{node.name}' must be lowercase with underscores"
                    )
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                # Variable names must be lowercase with underscores
                if not re.match(r'^[a-z][a-z0-9_]*$', node.id):
                    issues["errors"].append(
                        f"Variable '{node.id}' must be lowercase with underscores"
                    )

        return issues

    def _check_spacing(self, tree: ast.AST, code: str) -> Dict[str, List[str]]:
        """Check spacing according to COMP 1012 standards"""
        issues = {"errors": [], "warnings": []}

        # Check for spaces around operators
        lines = code.split('\n')
        operators = ['+', '-', '*', '/', '//', '%',
                     '**', '=', '==', '!=', '<', '>', '<=', '>=']

        for i, line in enumerate(lines, 1):
            for op in operators:
                if op in line and not line.strip().startswith('#'):
                    if f" {op} " not in line and op in line:
                        issues["errors"].append(
                            f"Line {i}: Missing spaces around '{op}' operator"
                        )

        return issues

    def _check_docstring(self, tree: ast.AST, code: str) -> Dict[str, List[str]]:
        """Check function docstrings"""
        issues = {"errors": [], "warnings": []}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if not docstring:
                    issues["errors"].append(
                        f"Function '{node.name}' must have a docstring"
                    )
                elif docstring and not docstring.strip().endswith('.'):
                    issues["warnings"].append(
                        f"Function '{node.name}' docstring should end with a period"
                    )

        return issues

    def _check_imports(self, tree: ast.AST, code: str) -> Dict[str, List[str]]:
        """Check import statements"""
        issues = {"errors": [], "warnings": []}

        import_nodes = [node for node in ast.walk(tree)
                        if isinstance(node, (ast.Import, ast.ImportFrom))]

        # All imports should be at the top
        if import_nodes:
            first_import = min(node.lineno for node in import_nodes)
            for node in ast.walk(tree):
                if hasattr(node, 'lineno'):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        continue
                    if node.lineno < first_import:
                        issues["errors"].append(
                            "All imports must be at the top of the file"
                        )
                        break

        return issues
