
from graph.state import MeetingState
from prompts.analysis_prompt import ANALYSIS_PROMPT
from services.llm_service import get_llm
from schemas.meeting import MeetingResult
from prompts.extraction_prompt import EXTRACTION_PROMPT
from schemas.meeting import ActionItem
from schemas.meeting import ActionExtraction

def validate_input(state: MeetingState) -> dict:
    transcript = state.get("transcript", "")

    if not isinstance(transcript, str) or not transcript.strip():
        return {
            "is_input_valid": False,
            "error": "Please provide a meeting transcript."
        }

    cleaned = transcript.strip()

    if len(cleaned) < 20:
        return {
            "is_input_valid": False,
            "error": "Transcript is too short. Please provide more meeting details."
        }

    return {
        "is_input_valid": True,
        "error": None
    }



def preprocess(state: MeetingState) -> dict:
    """
    Clean the transcript before analysis.
    """

    transcript = state["transcript"]

    cleaned_transcript = " ".join(transcript.split())

    return {
        "cleaned_transcript": cleaned_transcript
    }


def analyze_meeting(state: MeetingState) -> dict:
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(
            MeetingResult,
            method="json_schema"
        )

        prompt = ANALYSIS_PROMPT.format(
            transcript=state["cleaned_transcript"]
        )

        result = structured_llm.invoke(prompt)

        return {
            "summary": result.summary,
            "key_topics": result.key_topics,
            "decisions": result.decisions,
            "open_questions": result.open_questions,
            "processing_failed": False
        }

    except Exception:
        return {
            "processing_failed": True,
            "error": (
                "Meeting analysis failed. Check that Ollama is running "
                "and the configured model is available."
            )
        }


def extract_actions(state: MeetingState) -> dict:
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(
            ActionExtraction,
            method="json_schema"
        )

        prompt = EXTRACTION_PROMPT.format(
            transcript=state["cleaned_transcript"]
        )

        result = structured_llm.invoke(prompt)

        return {
            "action_items": result.action_items,
            "processing_failed": False
        }

    except Exception:
        return {
            "processing_failed": True,
            "error": (
                "Action extraction failed. Check that Ollama is running "
                "and the configured model is available."
            )
        }


def validate_output(state: MeetingState) -> dict:
    """
    Validate the generated action items.
    """

    errors = []
    action_items = state.get("action_items", [])

    for index, action in enumerate(action_items):
        if not action.task.strip():
            errors.append(
                f"Action item {index + 1} has an empty task."
            )

        if not action.source_text.strip():
            errors.append(
                f"Action item {index + 1} has no source evidence."
            )

    return {
        "validation_errors": errors,
        "is_valid": len(errors) == 0
    }

def prepare_retry(state: MeetingState) -> dict:
    """Increment the retry counter before regenerating the output."""
    current_retry_count = state.get("retry_count", 0)

    return {
        "retry_count": current_retry_count + 1
    }


def mark_validation_failure(state: MeetingState) -> dict:
    existing_error = state.get("error")

    if existing_error:
        return {"error": existing_error}

    errors = state.get("validation_errors", [])

    return {
        "error": "Output validation failed: " + "; ".join(errors)
    }




def check_guardrails(state: MeetingState) -> dict:
    """
    Check whether extracted evidence actually appears in the transcript.
    """
    transcript = " ".join(
        state["cleaned_transcript"].lower().split()
    )

    issues = []

    for index, action in enumerate(state.get("action_items", [])):
        evidence = " ".join(action.source_text.lower().split())

        if evidence not in transcript:
            issues.append(
                f"Action item {index + 1}: source evidence not found in transcript."
            )

    for index, decision in enumerate(state.get("decisions", [])):
        evidence = " ".join(decision.source_text.lower().split())

        if evidence not in transcript:
            issues.append(
                f"Decision {index + 1}: source evidence not found in transcript."
            )

    return {"guardrail_issues": issues}


def finalize_result(state: MeetingState) -> dict:
    """
    Build the final structured meeting result.
    """
    result = MeetingResult(
        summary=state["summary"],
        key_topics=state.get("key_topics", []),
        decisions=state.get("decisions", []),
        action_items=state.get("action_items", []),
        open_questions=state.get("open_questions", [])
    )

    return {"final_result": result}