from click.testing import CliRunner
from mastery.cli import cli
from mastery.models import db, Problem


def test_add_problem(app):
    with app.app_context():
        runner = CliRunner()
        result = runner.invoke(cli, ['add-problem', '--topic', 'BASICS'])
        assert result.exit_code == 0
        assert 'Created problem' in result.output


def test_show_progress(app):
    with app.app_context():
        # Create test data first
        problem = Problem(
            topic="BASICS",
            week=1,
            difficulty=1,
            description="Test problem",
            test_cases=[],
            starter_code=""
        )
        db.session.add(problem)
        db.session.commit()

        runner = CliRunner()
        result = runner.invoke(cli, ['show-progress', 'test_user'])
        assert result.exit_code == 0
        assert 'total_attempts' in result.output


def test_init_db(app):
    with app.app_context():
        runner = CliRunner()
        result = runner.invoke(cli, ['init-db'])
        assert result.exit_code == 0
        assert 'Database initialized' in result.output
