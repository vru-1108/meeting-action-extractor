
from typing import TypedDict
from typing_extensions import NotRequired

from schemas.meeting import MeetingResult, ActionItem, Decision


class MeetingState(TypedDict):

    # Original input
    transcript: str

    # Preprocessing
    is_input_valid: NotRequired[bool]
    cleaned_transcript: NotRequired[str]

    # Meeting analysis
    summary: NotRequired[str]
    key_topics: NotRequired[list[str]]
    decisions: NotRequired[list[Decision]]
    open_questions: NotRequired[list[str]]

    # Action extraction
    action_items: NotRequired[list[ActionItem]]

    # Validation
    validation_errors: NotRequired[list[str]]
    retry_count: NotRequired[int]
    is_valid: NotRequired[bool]

    # Guardrails
    guardrail_issues: NotRequired[list[str]]

    # Final output
    final_result: NotRequired[MeetingResult]
    error: NotRequired[str]
    processing_failed: NotRequired[bool]
