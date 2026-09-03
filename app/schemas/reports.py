from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ReportRead(BaseModel):
    id: int
    period_start: date
    period_end: date
    content_md: str
    content_html: str
    summary: dict
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
