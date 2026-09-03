from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.comment import PostCommentRead


class CollectRequest(BaseModel):
    platform: str = Field(default="xiaohongshu", examples=["xiaohongshu", "douyin"])
    keyword: str = "AI 工具"
    limit: int = Field(default=20, ge=1, le=100)


class CrawlPostRead(BaseModel):
    id: int
    platform: str
    post_id: str
    title: str
    content: str
    author: str
    url: str
    tags: list[str]
    metrics: dict[str, Any]
    published_at: datetime | None
    collected_at: datetime
    comments: list[PostCommentRead] = []

    model_config = {"from_attributes": True}
