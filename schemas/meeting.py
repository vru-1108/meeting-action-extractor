
from typing import Optional, Literal
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[Literal["high", "medium", "low"]] = None
    source_text: str
    status: Literal["pending", "completed"] = "pending"

class ActionExtraction(BaseModel):
    action_items: list[ActionItem] = Field(default_factory=list)

class Decision(BaseModel):
    decision: str
    source_text: str


class MeetingResult(BaseModel):
    summary: str

    key_topics: list[str] = Field(default_factory=list)

    decisions: list[Decision] = Field(default_factory=list)

    action_items: list[ActionItem] = Field(default_factory=list)

    open_questions: list[str] = Field(default_factory=list)
