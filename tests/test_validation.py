from graph.nodes import validate_output
from schemas.meeting import ActionItem


def test_valid_output():
    state = {
        "action_items": [
            ActionItem(
                task="Prepare the API documentation",
                owner="Rahul",
                source_text="Rahul will prepare the API documentation."
            )
        ]
    }

    result = validate_output(state)

    assert result["is_valid"] is True
    assert result["validation_errors"] == []


def test_empty_action_task():
    state = {
        "action_items": [
            ActionItem(
                task="",
                source_text="Rahul will prepare the API documentation."
            )
        ]
    }

    result = validate_output(state)

    assert result["is_valid"] is False
    assert "Action item 1 has an empty task." in result["validation_errors"]


def test_missing_source_evidence():
    state = {
        "action_items": [
            ActionItem(
                task="Prepare the API documentation",
                source_text=""
            )
        ]
    }

    result = validate_output(state)

    assert result["is_valid"] is False
    assert "Action item 1 has no source evidence." in result["validation_errors"]