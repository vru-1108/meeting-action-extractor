
from graph.nodes import extract_actions


def test_extract_actions():

    state = {
        "transcript": (
            "Sarah will complete API integration by Wednesday."
        ),
        "cleaned_transcript": (
            "Sarah will complete API integration by Wednesday."
        )
    }

    result = extract_actions(state)

    assert isinstance(result["action_items"], list)

    if result["action_items"]:
        action = result["action_items"][0]

        assert action.task
        assert action.source_text
