from flask import session
from datetime import datetime


def track_problem_attempt(problem_id: int, correct: bool):
    """Track problem attempt in session"""
    if 'problem_attempts' not in session:
        session['problem_attempts'] = {}

    if str(problem_id) not in session['problem_attempts']:
        session['problem_attempts'][str(problem_id)] = {
            'attempts': 0,
            'solved': False,
            'last_attempt': None
        }

    session['problem_attempts'][str(problem_id)]['attempts'] += 1
    if correct:
        session['problem_attempts'][str(problem_id)]['solved'] = True
    session['problem_attempts'][str(
        problem_id)]['last_attempt'] = datetime.utcnow().isoformat()
    session.modified = True


def get_problem_progress(problem_id: int) -> dict:
    """Get problem progress from session"""
    if 'problem_attempts' not in session:
        return {'attempts': 0, 'solved': False, 'last_attempt': None}

    return session['problem_attempts'].get(str(problem_id),
                                           {'attempts': 0, 'solved': False, 'last_attempt': None})
