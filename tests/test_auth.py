import json
import pytest
from mastery.models.user import User
from mastery.models import db


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()

        # Get the user ID to ensure it's committed
        user_id = user.id
        yield user

        # Cleanup
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()


def test_register(client):
    response = client.post('/auth/register',
                           json={'username': 'newuser', 'password': 'newpass'})
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.post('/auth/login',
                           json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200


def test_login_invalid(client):
    response = client.post('/auth/login',
                           json={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 401


def test_logout(client, test_user):
    # Login first
    client.post('/auth/login',
                json={'username': 'testuser', 'password': 'testpass'})
    # Then logout
    response = client.get('/auth/logout')
    assert response.status_code == 200
