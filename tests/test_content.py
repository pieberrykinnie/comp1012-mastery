import pytest
from mastery.content import ContentManager


def test_content_manager_initialization():
    manager = ContentManager()
    assert len(manager.weeks) == 11
    assert all(1 <= week <= 11 for week in manager.weeks)


def test_get_week_content(app):
    with app.app_context():
        manager = ContentManager()
        content = manager.get_week_content(1)
        assert content["topic"] == "BASICS"
        assert "variables" in content["subtopics"]
        assert isinstance(content["problems"], list)


def test_invalid_week():
    manager = ContentManager()
    with pytest.raises(ValueError):
        manager.get_week_content(12)
