from typing import Dict, Any
from .base import ProblemTemplate
import numpy as np


class MatrixProblemTemplate(ProblemTemplate):
    def generate(self) -> Dict[str, Any]:
        if self.difficulty == 1:
            return {
                "description": "Write a function that calculates the transpose of a matrix",
                "test_cases": [
                    {
                        "input": "matrix_transpose(np.array([[1, 2], [3, 4]]))",
                        "expected": np.array([[1, 3], [2, 4]])
                    },
                    {
                        "input": "matrix_transpose(np.array([[1, 2, 3], [4, 5, 6]]))",
                        "expected": np.array([[1, 4], [2, 5], [3, 6]])
                    }
                ],
                "starter_code": "def matrix_transpose(matrix):\n    # Your code here\n    pass",
                "solution": "import numpy as np\n\ndef matrix_transpose(matrix):\n    return np.transpose(matrix)"
            }
        elif self.difficulty == 2:
            return {
                "description": "Write a function that performs matrix multiplication",
                "test_cases": [
                    {
                        "input": "matrix_multiply(np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]]))",
                        "expected": np.array([[19, 22], [43, 50]])
                    },
                    {
                        "input": "matrix_multiply(np.array([[1, 0], [0, 1]]), np.array([[2, 2], [2, 2]]))",
                        "expected": np.array([[2, 2], [2, 2]])
                    }
                ],
                "starter_code": "def matrix_multiply(matrix1, matrix2):\n    # Your code here\n    pass",
                "solution": "import numpy as np\n\ndef matrix_multiply(matrix1, matrix2):\n    return np.matmul(matrix1, matrix2)"
            }
