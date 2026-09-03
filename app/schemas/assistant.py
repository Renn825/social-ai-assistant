from typing import Any

from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    message: str = Field(min_length=1)


class AssistantResponse(BaseModel):
    answer: str
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)

