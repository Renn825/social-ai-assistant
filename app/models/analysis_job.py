from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class AnalysisJob(SQLModel, table=True):
    __tablename__ = "analysis_jobs"

    id: int | None = Field(default=None, primary_key=True)
    status: str = Field(default="pending", index=True)
    note_ids: list[int] = Field(default_factory=list, sa_column=Column(JSON))
    model: str = Field(default="")
    result: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))
    error: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
