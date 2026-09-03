from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


class CrawlTask(SQLModel, table=True):
    __tablename__ = "crawl_tasks"

    id: int | None = Field(default=None, primary_key=True)
    platform: str = Field(index=True)
    keyword: str
    limit: int = Field(default=20)
    status: TaskStatus = Field(default=TaskStatus.pending, index=True)
    total: int = Field(default=0)
    succeeded: int = Field(default=0)
    failed: int = Field(default=0)
    error: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    finished_at: datetime | None = None

