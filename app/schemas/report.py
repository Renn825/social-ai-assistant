from datetime import datetime

from pydantic import BaseModel, Field


class ReportRequest(BaseModel):
    platform: str = Field(default="xiaohongshu")
    report_date: str = Field(default="")
    style: str = Field(default="weekly", examples=["weekly", "daily"])


class AnalysisReportRead(BaseModel):
    id: int
    title: str
    platform: str
    report_date: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}

