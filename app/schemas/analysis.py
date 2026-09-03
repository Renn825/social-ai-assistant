from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    platform: str | None = Field(default=None, description="xiaohongshu / douyin")
    start_date: str | None = None
    end_date: str | None = None


class AnalysisJobRead(BaseModel):
    id: int
    status: str
    result: dict | None
    error: str | None
    created_at: datetime

    class Config:
        from_attributes = True
