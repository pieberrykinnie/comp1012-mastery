import pytest
import json
from mastery.api import create_app
from mastery.models import db


@pytest.fixture(scope='module')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    return app


@pytest.fixture(scope='function')  # Changed to function scope
def client(app):
    with app.app_context():  # Use context manager instead
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_get_problems(client):
    response = client.get('/api/problems/BASICS')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_nonexistent_problem(client):
    response = client.get('/api/problems/999')
    assert response.status_code == 404


def test_submit_solution(app, client):
    from mastery.repository import ProblemRepository

    repo = ProblemRepository()
    problem = repo.create_problem("BASICS", 1)

    response = client.post(
        f'/api/submit/{problem.id}',
        json={
            'user_id': 'test_user',
            'code': 'def celsius_to_fahrenheit(celsius):\n    return (celsius * 9/5) + 32'
        }
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'correct' in data
    assert 'attempts' in data
