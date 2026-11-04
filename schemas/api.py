from pydantic import BaseModel, Field
from schemas.meeting import MeetingResult


class MeetingRequest(BaseModel):
    transcript: str = Field(
        min_length=1,
        description="Meeting transcript to analyze"
    )


class MeetingResponse(BaseModel):
    success: bool
    result: MeetingResult
    guardrail_issues: list[str] = Field(default_factory=list)