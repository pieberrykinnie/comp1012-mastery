from typing import List, Dict
from functools import wraps
from .cache import problem_cache, progress_cache, stats_cache
from .models import db, Problem
from .models.progress import UserProgress


def cache_problem_results(func):
    """Decorator to cache problem validation results"""
    @wraps(func)
    def wrapper(self, user_id: str, problem_id: int, code: str) -> Dict:
        cache_key = f"result_{user_id}_{problem_id}_{hash(code)}"
        cached = progress_cache.get(cache_key)
        if cached:
            return cached

        result = func(self, user_id, problem_id, code)
        progress_cache.set(cache_key, result)
        return result
    return wrapper


def cache_user_stats(func):
    """Decorator to cache user statistics"""
    @wraps(func)
    def wrapper(self, user_id: str) -> Dict:
        cache_key = f"stats_{user_id}"
        cached = stats_cache.get(cache_key)
        if cached:
            return cached

        result = func(self, user_id)
        stats_cache.set(cache_key, result)
        return result
    return wrapper


class BatchProcessor:
    """Handle batch operations efficiently"""

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size

    def process_submissions(self, submissions: List[Dict]) -> List[Dict]:
        """Process multiple submissions in batches"""
        results = []
        for i in range(0, len(submissions), self.batch_size):
            batch = submissions[i:i + self.batch_size]
            results.extend(self._process_batch(batch))
        return results

    def _process_batch(self, batch: List[Dict]) -> List[Dict]:
        """Process a single batch of submissions"""
        from .validator import ProblemValidator
        validator = ProblemValidator()

        results = []
        for submission in batch:
            try:
                # Updated to use Session.get()
                problem = db.session.get(Problem, submission['problem_id'])
                if not problem:
                    results.append({
                        'submission_id': submission.get('id'),
                        'error': 'Problem not found'
                    })
                    continue

                is_correct = validator.validate_solution(
                    submission['code'],
                    problem.test_cases
                )

                results.append({
                    'submission_id': submission.get('id'),
                    'correct': is_correct
                })
            except Exception as e:
                results.append({
                    'submission_id': submission.get('id'),
                    'error': str(e)
                })

        return results
