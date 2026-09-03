from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisJobCreate(BaseModel):
    note_ids: list[int] = Field(min_length=1)


class AnalysisJobRead(BaseModel):
    id: int
    status: str
    note_ids: list[int]
    model: str
    result: dict | None = None
    error: str | None = None
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}
