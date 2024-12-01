import pytest
from click.testing import CliRunner
from mastery.cli import cli
from mastery.models import db, Problem
from mastery.models.progress import UserProgress
from mastery.repository import ProblemRepository
from mastery.tracker import ProgressTracker


class TestCompleteLearningPath:
    @pytest.fixture(autouse=True)
    def setup(self, app):
        """Setup test environment with initial problems"""
        self.app = app
        self.runner = CliRunner()
        self.user_id = "test_student"

    def test_complete_learning_path(self, app):
        """Test complete student learning journey"""
        with app.app_context():
            # Create initial problems
            problem = Problem(
                topic="BASICS",
                week=1,
                difficulty=1,
                description="Calculate area of a circle",
                test_cases=[
                    {"input": "circle_area(1.0)",
                     "expected": 3.141592653589793}
                ],
                starter_code="def circle_area(radius):\n    pass"
            )
            db.session.add(problem)
            db.session.commit()

            # 1. Initial progress check
            result = self.runner.invoke(cli, ['show-progress', self.user_id])
            assert result.exit_code == 0
            assert '"total_attempts": 0' in result.output

            # 2. Get initial recommendations
            result = self.runner.invoke(
                cli, ['get-recommendations', self.user_id])
            assert result.exit_code == 0
            assert 'BASICS' in result.output

            # 3. Submit solution
            tracker = ProgressTracker()
            result = tracker.record_attempt(
                self.user_id,
                problem.id,
                "def circle_area(radius):\n    import math\n    return math.pi * radius ** 2"
            )
            assert result["correct"] == True

            # 4. Get feedback
            result = self.runner.invoke(cli, ['get-feedback', self.user_id])
            assert result.exit_code == 0
            assert 'overall_progress' in result.output

    def test_struggling_student_path(self, app):
        """Test system's response to a struggling student"""
        with app.app_context():
            # Create test problem
            problem = Problem(
                topic="BASICS",
                week=1,
                difficulty=1,
                description="Test problem",
                test_cases=[
                    {"input": "circle_area(1.0)", "expected": 3.141592653589793}],
                starter_code="def circle_area(radius):\n    pass"
            )
            db.session.add(problem)
            db.session.commit()

            # Make multiple failed attempts
            tracker = ProgressTracker()
            for _ in range(3):
                result = tracker.record_attempt(
                    self.user_id,
                    problem.id,
                    "def circle_area(radius):\n    return radius"
                )
                assert result["correct"] == False

            result = self.runner.invoke(cli, ['get-feedback', self.user_id])
            assert result.exit_code == 0
            assert 'suggested_actions' in result.output

    def test_advanced_student_path(self, app):
        """Test system's handling of fast-progressing students"""
        with app.app_context():
            # Create test problems
            problems = []
            for i, topic in enumerate(["BASICS", "STRINGS_IO"]):
                problem = Problem(
                    topic=topic,
                    week=i+1,
                    difficulty=1,
                    description=f"Test problem {i}",
                    test_cases=[{"input": "test()", "expected": True}],
                    starter_code="def test():\n    pass"
                )
                db.session.add(problem)
                problems.append(problem)
            db.session.commit()

            # Solve problems quickly
            tracker = ProgressTracker()
            for problem in problems:
                result = tracker.record_attempt(
                    self.user_id,
                    problem.id,
                    "def test():\n    return True"
                )
                assert result["correct"] == True

            result = self.runner.invoke(
                cli, ['get-recommendations', self.user_id])
            assert result.exit_code == 0
