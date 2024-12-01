from mastery.constants import TOPICS


def test_topic_structure():
    assert len(TOPICS) == 11
    assert all(isinstance(TOPICS[topic]["week"], int) for topic in TOPICS)
    assert all(isinstance(TOPICS[topic]["subtopics"], list)
               for topic in TOPICS)
    assert all(1 <= TOPICS[topic]["week"] <= 11 for topic in TOPICS)


def test_topic_progression():
    for topic in TOPICS:
        week = TOPICS[topic]["week"]
        assert week > 0
        assert len(TOPICS[topic]["subtopics"]) > 0
