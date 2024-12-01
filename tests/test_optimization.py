from datetime import datetime
import time
from mastery.cache import CacheManager, get_problem_template
from mastery.optimization import BatchProcessor
from mastery.models import db, Problem


def test_cache_manager():
    cache = CacheManager(ttl_seconds=1)
    cache.set("test_key", "test_value")

    assert cache.get("test_key") == "test_value"
    time.sleep(1.1)  # Wait for TTL to expire
    assert cache.get("test_key") is None


def test_problem_template_cache(app):
    with app.app_context():
        # First call should create template
        template1 = get_problem_template("BASICS", 1)
        # Second call should return cached template
        template2 = get_problem_template("BASICS", 1)

        assert template1 == template2


def test_batch_processor(app):
    with app.app_context():
        # Create test problem
        problem = Problem(
            topic="BASICS",
            week=1,
            difficulty=1,
            description="Test problem",
            test_cases=[{"input": "test()", "expected": True}],
            starter_code="def test():\n    pass"
        )
        db.session.add(problem)
        db.session.commit()

        processor = BatchProcessor(batch_size=2)
        submissions = [
            {
                'id': 1,
                'problem_id': problem.id,
                'code': 'def test():\n    return True'
            },
            {
                'id': 2,
                'problem_id': problem.id,
                'code': 'def test():\n    return False'
            }
        ]

        results = processor.process_submissions(submissions)
        assert len(results) == 2
        assert all('submission_id' in r for r in results)
