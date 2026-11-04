
from graph.nodes import analyze_meeting


def test_analyze_meeting():

    state = {
        "transcript": "Sarah will complete API integration by Wednesday.",
        "cleaned_transcript": (
            "Sarah will complete API integration by Wednesday."
        )
    }

    result = analyze_meeting(state)

    assert isinstance(result["summary"], str)
    assert isinstance(result["key_topics"], list)
    assert isinstance(result["decisions"], list)
    assert isinstance(result["open_questions"], list)
