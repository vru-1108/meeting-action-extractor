from graph.nodes import prepare_retry, mark_validation_failure
from graph.edges import route_after_validation


def test_prepare_retry():
    state = {"retry_count": 0}

    result = prepare_retry(state)

    assert result["retry_count"] == 1


def test_prepare_retry_when_count_missing():
    state = {}

    result = prepare_retry(state)

    assert result["retry_count"] == 1


def test_route_to_guardrails_when_valid():
    state = {
        "is_valid": True,
        "retry_count": 0
    }

    assert route_after_validation(state) == "guardrails"


def test_route_to_retry_when_invalid_and_retry_available():
    state = {
        "is_valid": False,
        "retry_count": 0
    }

    assert route_after_validation(state) == "retry"


def test_route_to_failure_when_retry_exhausted():
    state = {
        "is_valid": False,
        "retry_count": 1
    }

    assert route_after_validation(state) == "failed"


def test_mark_validation_failure():
    state = {
        "validation_errors": ["Meeting summary is missing."]
    }

    result = mark_validation_failure(state)

    assert "Meeting summary is missing." in result["error"]