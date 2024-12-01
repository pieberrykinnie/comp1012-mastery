from mastery.constants import TOPICS


def test_topics_structure():
    assert "BASICS" in TOPICS
    assert "week" in TOPICS["BASICS"]
    assert "subtopics" in TOPICS["BASICS"]
    assert isinstance(TOPICS["BASICS"]["subtopics"], list)
