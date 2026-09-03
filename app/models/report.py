from datetime import datetime

from sqlmodel import Field, SQLModel


class AnalysisReport(SQLModel, table=True):
    __tablename__ = "analysis_reports"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    platform: str = Field(index=True)
    report_date: str = Field(index=True)
    format: str = Field(default="markdown")
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
