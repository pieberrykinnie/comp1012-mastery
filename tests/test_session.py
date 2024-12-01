import pytest
from datetime import datetime
from flask import session
from mastery.session import track_problem_attempt, get_problem_progress


def test_track_new_problem_attempt(app):
    """Test tracking a new problem attempt"""
    with app.test_request_context():
        track_problem_attempt(1, False)

        assert 'problem_attempts' in session
        assert '1' in session['problem_attempts']
        assert session['problem_attempts']['1']['attempts'] == 1
        assert not session['problem_attempts']['1']['solved']
        assert isinstance(datetime.fromisoformat(
            session['problem_attempts']['1']['last_attempt']),
            datetime)


def test_track_multiple_attempts(app):
    """Test tracking multiple attempts for the same problem"""
    with app.test_request_context():
        # First attempt - incorrect
        track_problem_attempt(1, False)
        assert session['problem_attempts']['1']['attempts'] == 1
        assert not session['problem_attempts']['1']['solved']

        # Second attempt - correct
        track_problem_attempt(1, True)
        assert session['problem_attempts']['1']['attempts'] == 2
        assert session['problem_attempts']['1']['solved']


def test_track_multiple_problems(app):
    """Test tracking attempts for different problems"""
    with app.test_request_context():
        track_problem_attempt(1, True)
        track_problem_attempt(2, False)

        assert '1' in session['problem_attempts']
        assert '2' in session['problem_attempts']
        assert session['problem_attempts']['1']['solved']
        assert not session['problem_attempts']['2']['solved']


def test_get_problem_progress_new(app):
    """Test getting progress for a new problem"""
    with app.test_request_context():
        progress = get_problem_progress(1)
        assert progress['attempts'] == 0
        assert not progress['solved']
        assert progress['last_attempt'] is None


def test_get_problem_progress_existing(app):
    """Test getting progress for an attempted problem"""
    with app.test_request_context():
        track_problem_attempt(1, True)
        progress = get_problem_progress(1)

        assert progress['attempts'] == 1
        assert progress['solved']
        assert isinstance(datetime.fromisoformat(progress['last_attempt']),
                          datetime)
