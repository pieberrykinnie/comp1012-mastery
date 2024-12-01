import pytest
from flask import jsonify
from werkzeug.exceptions import NotFound, BadRequest
from mastery.errors import MasteryError, handle_error


def test_mastery_error():
    """Test custom MasteryError"""
    error = MasteryError("Invalid input", status_code=400)
    assert error.message == "Invalid input"
    assert error.status_code == 400
    assert error.to_dict() == {'error': 'Invalid input'}


def test_handle_mastery_error(app):
    """Test handling MasteryError"""
    with app.test_request_context():
        error = MasteryError("Test error", status_code=400)
        response = handle_error(error)
        data = response.get_json()

        assert response.status_code == 400
        assert data['error'] == "Test error"


def test_handle_http_exception(app):
    """Test handling HTTP exceptions"""
    with app.test_request_context():
        error = NotFound("Resource not found")
        response = handle_error(error)
        data = response.get_json()

        assert response.status_code == 404
        assert data['error'] == "Resource not found"


def test_handle_unexpected_error(app):
    """Test handling unexpected exceptions"""
    with app.test_request_context():
        error = ValueError("Unexpected error")
        response = handle_error(error)
        data = response.get_json()

        assert response.status_code == 500
        assert data['error'] == "An unexpected error occurred"


def test_error_logging(app, caplog):
    """Test error logging functionality"""
    with app.test_request_context():
        error = MasteryError("Test log error")
        handle_error(error)

        assert "Test log error" in caplog.text
        assert "MasteryError" in caplog.text
