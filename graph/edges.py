def route_after_validation(state):
    if state.get("is_valid", False):
        return "guardrails"

    retry_count = state.get("retry_count", 0)

    if retry_count < 1:
        return "retry"

    return "failed"

def route_after_processing(state: dict) -> str:
    if state.get("processing_failed", False):
        return "failed"

    return "continue"