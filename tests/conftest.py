import pytest
from mastery.api import create_app
from mastery.models import db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-key'
    })
    return app


@pytest.fixture
def client(app):
    with app.app_context():  # Use context manager instead of push/pop
        db.create_all()
        with app.test_client() as client:
            yield client
            db.session.remove()
            db.drop_all()
