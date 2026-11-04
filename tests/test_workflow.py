from graph.workflow import build_workflow
from graph.nodes import get_llm
from schemas.meeting import (
    MeetingResult,
    ActionItem,
    ActionExtraction
)


class FakeRunnable:
    def __init__(self, response):
        self.response = response

    def invoke(self, prompt):
        return self.response.pop(0)


class FakeLLM:
    def __init__(self, responses):
        self.responses = responses

    def with_structured_output(self, schema, **kwargs):
        return FakeRunnable(self.responses[schema])


def test_complete_workflow(monkeypatch):

    responses = {
        MeetingResult: [
            MeetingResult(
                summary="The team discussed API integration.",
                key_topics=["API integration"],
                decisions=[],
                open_questions=[]
            )
        ],
        ActionExtraction: [
            ActionExtraction(
                action_items=[
                    ActionItem(
                        task="Complete API integration",
                        owner="Sarah",
                        deadline="Wednesday",
                        source_text=(
                            "Sarah will complete API integration by Wednesday."
                        )
                    )
                ]
            )
        ]
    }

    monkeypatch.setattr(
        "graph.nodes.get_llm",
        lambda: FakeLLM(responses)
    )

    app = build_workflow()

    result = app.invoke({
        "transcript": (
            "Sarah will complete API integration by Wednesday."
        ),
        "retry_count": 0
    })

    assert result["is_valid"] is True
    assert result["retry_count"] == 0
    assert result["guardrail_issues"] == []
    assert isinstance(result["final_result"], MeetingResult)

    assert len(result["final_result"].action_items) == 1
    assert result["final_result"].action_items[0].owner == "Sarah"

def test_workflow_retries_after_invalid_output(monkeypatch):

    responses = {
        MeetingResult: [
            MeetingResult(
                summary="The team discussed API integration.",
                key_topics=["API integration"],
                decisions=[],
                open_questions=[]
            ),
            MeetingResult(
                summary="The team discussed API integration.",
                key_topics=["API integration"],
                decisions=[],
                open_questions=[]
            )
        ],
        ActionExtraction: [
            # First attempt: invalid action item
            ActionExtraction(
                action_items=[
                    ActionItem(
                        task="",
                        owner="Sarah",
                        deadline="Wednesday",
                        source_text=""
                    )
                ]
            ),
            # Second attempt: valid action item
            ActionExtraction(
                action_items=[
                    ActionItem(
                        task="Complete API integration",
                        owner="Sarah",
                        deadline="Wednesday",
                        source_text=(
                            "Sarah will complete API integration by Wednesday."
                        )
                    )
                ]
            )
        ]
    }

    monkeypatch.setattr(
        "graph.nodes.get_llm",
        lambda: FakeLLM(responses)
    )

    app = build_workflow()

    result = app.invoke({
        "transcript": (
            "Sarah will complete API integration by Wednesday."
        ),
        "retry_count": 0
    })

    assert result["retry_count"] == 1
    assert result["is_valid"] is True
    assert result["validation_errors"] == []
    assert len(result["final_result"].action_items) == 1