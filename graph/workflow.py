from langgraph.graph import StateGraph, START, END

from graph.state import MeetingState
from graph.nodes import (
    validate_input,
    preprocess,
    analyze_meeting,
    extract_actions,
    validate_output,
    prepare_retry,
    mark_validation_failure,
    check_guardrails,
    finalize_result
)

from graph.edges import (
    route_after_validation,
    route_after_processing
)


def route_after_input_validation(state: MeetingState) -> str:
    if state.get("is_input_valid", False):
        return "valid"
    return "invalid"


def build_workflow():
    workflow = StateGraph(MeetingState)

    # Register nodes
    workflow.add_node("validate_input", validate_input)
    workflow.add_node("preprocess", preprocess)
    workflow.add_node("analyze_meeting", analyze_meeting)
    workflow.add_node("extract_actions", extract_actions)
    workflow.add_node("validate_output", validate_output)
    workflow.add_node("prepare_retry", prepare_retry)
    workflow.add_node("mark_validation_failure", mark_validation_failure)
    workflow.add_node("guardrails", check_guardrails)
    workflow.add_node("finalize", finalize_result)

    # Starting point
    workflow.add_edge(START, "validate_input")

    # Input validation routing
    workflow.add_conditional_edges(
        "validate_input",
        route_after_input_validation,
        {
            "valid": "preprocess",
            "invalid": END
        }
    )

    # Main processing flow
    workflow.add_edge("preprocess", "analyze_meeting")
    workflow.add_conditional_edges(
    "analyze_meeting",
    route_after_processing,
    {
        "continue": "extract_actions",
        "failed": "mark_validation_failure"
    }
)

    workflow.add_conditional_edges(
    "extract_actions",
    route_after_processing,
    {
        "continue": "validate_output",
        "failed": "mark_validation_failure"
    }
)

    # Output validation routing
    workflow.add_conditional_edges(
        "validate_output",
        route_after_validation,
        {
            "guardrails": "guardrails",
            "retry": "prepare_retry",
            "failed": "mark_validation_failure"
        }
    )

    # Retry flow
    workflow.add_edge("prepare_retry", "analyze_meeting")

    # Successful flow
    workflow.add_edge("guardrails", "finalize")
    workflow.add_edge("finalize", END)

    # Failed validation flow
    workflow.add_edge("mark_validation_failure", END)

    return workflow.compile()