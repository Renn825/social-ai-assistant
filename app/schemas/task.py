from datetime import datetime

from pydantic import BaseModel, Field

from app.models.task import TaskStatus


class CrawlTaskCreate(BaseModel):
    platform: str
    keyword: str
    limit: int = Field(default=20, ge=1, le=100)


class CrawlTaskRead(BaseModel):
    id: int
    platform: str
    keyword: str
    limit: int
    status: TaskStatus
    total: int
    succeeded: int
    failed: int
    error: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = {"from_attributes": True}

