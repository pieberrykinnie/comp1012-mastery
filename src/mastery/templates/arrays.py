from typing import Dict, Any
from .base import ProblemTemplate
import numpy as np


class ArrayProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        if self.difficulty == 1:
            return {
                "description": "Write a function that calculates the mean of a NumPy array",
                "test_cases": [
                    {"input": "array_mean(np.array([1, 2, 3, 4, 5]))",
                     "expected": 3.0},
                    {"input": "array_mean(np.array([2.5, 7.5]))",
                     "expected": 5.0}
                ],
                "starter_code": "def array_mean(arr):\n    # Your code here\n    pass",
                "solution": "import numpy as np\n\ndef array_mean(arr):\n    return np.mean(arr)"
            }
        elif self.difficulty == 2:
            return {
                "description": "Write a function that finds all elements greater than the mean",
                "test_cases": [
                    {"input": "above_mean(np.array([1, 2, 3, 4, 5]))", "expected": [
                        4, 5]},
                    {"input": "above_mean(np.array([1.0, 1.5, 2.0, 2.5]))", "expected": [
                        2.0, 2.5]}
                ],
                "starter_code": "def above_mean(arr):\n    # Your code here\n    pass",
                "solution": "import numpy as np\n\ndef above_mean(arr):\n    return arr[arr > np.mean(arr)]"
            }
