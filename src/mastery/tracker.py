from datetime import datetime
from typing import List, Dict
from .models import db, Problem
from .models.progress import UserProgress
from .validator import ProblemValidator


class ProgressTracker:
    def __init__(self):
        self.validator = ProblemValidator()

    def record_attempt(self, user_id: str, problem_id: int, code: str) -> Dict:
        problem = db.session.get(Problem, problem_id)
        if not problem:
            raise ValueError("Problem not found")

        progress = UserProgress.query.filter_by(
            user_id=user_id,
            problem_id=problem_id
        ).first()

        if not progress:
            progress = UserProgress(
                user_id=user_id,
                problem_id=problem_id,
                attempts=0  # Explicitly initialize attempts
            )
            db.session.add(progress)
            db.session.commit()  # Commit to ensure the record exists

        is_correct = self.validator.validate_solution(code, problem.test_cases)
        progress.attempts += 1
        progress.solved = is_correct
        progress.last_attempt = datetime.utcnow()

        db.session.commit()

        return {
            "correct": is_correct,
            "attempts": progress.attempts
        }

    def get_user_progress(self, user_id: str) -> List[Dict]:
        progress = UserProgress.query.filter_by(user_id=user_id).all()
        return [
            {
                "problem_id": p.problem_id,
                "attempts": p.attempts,
                "solved": p.solved,
                "last_attempt": p.last_attempt
            }
            for p in progress
        ]
