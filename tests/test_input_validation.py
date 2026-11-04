
from graph.nodes import validate_input, preprocess


def test_empty_transcript():
    state = {"transcript": ""}

    result = validate_input(state)

    assert result["is_input_valid"] is False


def test_valid_transcript():
    state = {
        "transcript": "Sarah will complete API integration by Wednesday."
    }

    result = validate_input(state)

    assert result["is_input_valid"] is True


def test_preprocessing():
    state = {
        "transcript": "Sarah: Hello.   \n\n John: Hi."
    }

    result = preprocess(state)

    assert result["cleaned_transcript"] == "Sarah: Hello. John: Hi."
